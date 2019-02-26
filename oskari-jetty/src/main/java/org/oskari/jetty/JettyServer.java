package org.oskari.jetty;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.eclipse.jetty.plus.jndi.Resource;
import org.eclipse.jetty.server.HttpConnectionFactory;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.handler.ContextHandlerCollection;
import org.eclipse.jetty.webapp.Configuration;
import org.eclipse.jetty.webapp.WebAppContext;
import org.eclipse.jetty.websocket.jsr356.server.deploy.WebSocketServerContainerInitializer;

import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.sql.DataSource;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.*;
import java.util.stream.Stream;

public class JettyServer {

    public static final int DEFAULT_PORT = 8080;

    private Server server;
    private String classPath;
    private boolean isInitialized = false;
    private boolean parentClassLoaderPriority = true;
    private ContextHandlerCollection contexts = new ContextHandlerCollection();

    public void init() throws NamingException, ServletException {

        this.classPath = System.getenv("JETTY_CLASSPATH");

        int port = DEFAULT_PORT;
        String portStr = System.getenv("JETTY_PORT");
        if (portStr != null) {
            port = Integer.parseInt(portStr);
        }
        this.server = new Server(port);

        //Enable parsing of jndi-related parts of web.xml and jetty-env.xml
        Configuration.ClassList classlist = Configuration.ClassList.setServerDefault(server);
        classlist.addAfter("org.eclipse.jetty.webapp.FragmentConfiguration",
                "org.eclipse.jetty.plus.webapp.EnvConfiguration"
                , "org.eclipse.jetty.plus.webapp.PlusConfiguration");
        classlist.addBefore("org.eclipse.jetty.webapp.JettyWebXmlConfiguration",
                "org.eclipse.jetty.annotations.AnnotationConfiguration");

        // Logback access log instead of Jetty's build in logging to be able to log username
        EnhancedRequestLog requestLog = new EnhancedRequestLog();
        requestLog.setResource("/logback-access.xml");
        requestLog.setQuiet(true);
        server.setRequestLog(requestLog);

        server.setStopAtShutdown(true);

        // Remove Server header from HTTP-responses
        Stream.of(server.getConnectors()).flatMap(connector -> connector.getConnectionFactories().stream())
                .filter(connFactory -> connFactory instanceof HttpConnectionFactory)
                .forEach(httpConnFactory -> ((HttpConnectionFactory)httpConnFactory).getHttpConfiguration().setSendServerVersion(false));

        String transportWebappPath = System.getenv("TRANSPORT_WEBAPP");
        WebAppContext webappTransport = getWebApp("/transport", transportWebappPath);
        if (webappTransport != null) {
            contexts.addHandler(webappTransport);
        }

        server.setHandler(contexts);
        if (webappTransport != null) {
            WebSocketServerContainerInitializer.configureContext(webappTransport);
        }

        String oskariWebappPath = System.getenv("OSKARI_WEBAPP");
        WebAppContext webappOskari = getWebApp("/hkp", oskariWebappPath);
        if (webappOskari != null) {
            contexts.addHandler(webappOskari);
        }
        new Resource(server, "jdbc/OskariPool", getDatasource());
        this.isInitialized = true;
    }

    public void start() throws Exception {
        if (!isInitialized) {
            throw new IllegalStateException("init() must be called before start!");
        }
        server.start();
        //server.dumpStdErr();
        server.join();
    }

    public void stop() throws Exception {
        if (this.server != null) {
            this.server.stop();
        }
    }

    protected DataSource getDatasource() {
        Properties props = new Properties();
        try {
            props.load(JettyServer.class.getResourceAsStream("/db.properties"));
        } catch (IOException e) {
            throw new RuntimeException("Unable to load db.properties", e);
        }
        props.put("dataSource.logWriter", new PrintWriter(System.out));

        HikariConfig config = new HikariConfig(props);
        HikariDataSource dataSource = new HikariDataSource(config);
        return dataSource;
    }

    protected WebAppContext getWebApp(String contextPath, String webappPath) {
        if (webappPath != null) {
            File path = new File(webappPath);
            if (path.exists() && path.canRead()) {
                WebAppContext webapp = new WebAppContext();
                webapp.setContextPath(contextPath);
                webapp.setWar(webappPath);
                webapp.setParentLoaderPriority(parentClassLoaderPriority);
                if (this.classPath != null && !"".equals(this.classPath)) {
                    webapp.setExtraClasspath(this.classPath);
                }

                // Set the ContainerIncludeJarPattern so that jetty examines these
                // container-path jars for tlds, web-fragments etc.
                // If you omit the jar that contains the jstl .tlds, the jsp engine will
                // scan for them instead.
                webapp.setAttribute(
                        "org.eclipse.jetty.server.webapp.ContainerIncludeJarPattern",
                        ".*/[^/]*servlet-api-[^/]*\\.jar$|.*/javax.servlet.jsp.jstl-.*\\.jar$|.*/[^/]*taglibs.*\\.jar$" );

                return webapp;
            }
        }
        return null;
    }

    public static void main(String[] args) throws Exception {
        JettyServer jettyServer = new JettyServer();
        jettyServer.init();

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            try {
                jettyServer.stop();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }));

        jettyServer.start();
    }
}
