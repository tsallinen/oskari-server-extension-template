# Packaging Oskari as RPM

This is an experiment in packaging and distributing Oskari Server as RPM packages on Linux systems.

Build requirements: Red Hat Enterprise Linux (RHEL) 7, CentOS 7 or Fedora platform with rpmbuild, Java 8 JDK and Maven installed.

If necessary, rpmbuild can be installed with command

```bash
yum install rpm-build
```

## Building

First execute maven build as usual, then call the build-rpm.sh script:

```bash
mvn clean package
sh packages/rpm/build-rpm.sh
```

The created packages (oskari-jetty, oskari-map-webapp, oskari-transport-webapp) can be installed locally directly from disk:

```bash
yum install packages/rpm/RPMS/noarch/oskari-jetty-VERSION-RELEASE.el7.noarch.rpm
yum install packages/rpm/RPMS/noarch/oskari-map-webapp-VERSION-RELEASE.el7.noarch.rpm
yum install packages/rpm/RPMS/noarch/oskari-transport-webapp-VERSION-RELEASE.el7.noarch.rpm
```

These install other required packages (Java 8) as dependencies, but not other components, such as PostgreSQL or Redis.

A yum repository is recommended to distribute these packages.To distribute these packages.

The created packages inherit their VERSION from the one defined in the Maven root POM. If the Maven build produces a SNAPSHOT-version, RELEASE becomes 0.timestamp (0.yyyyMMddHHmmss), with Maven release versions "1".

## Service usage

Installing oskari-jetty package setups 'oskari-jetty' service, which can be started and enabled  as follows:

```bash
systemctl enable oskari-jetty
systemctl start oskari-jetty
```

Jetty server uses 8080 as default port, this can be configured.

### Configuration files

| Configuration file                               | Description                                                                   |
|--------------------------------------------------|-------------------------------------------------------------------------------|
| /etc/sysconfig/oskari-jetty                      | Jetty service configuration. Set Java startup parameters, http port etc. here |
| /etc/logrotate.d/oskari-jetty                    | Logrotate configuration                                                       | 
| /usr/share/jetty/resources/db.properties         | PostgreSQL connection properties                                              |
| /usr/share/jetty/resources/log4j.properties      | Common logging configuration                                                  |
| /usr/share/jetty/resources/logback-access.xml    | Access log configuration                                                      |
| /usr/share/jetty/resources/oskari-ext.properties | Environment specific oskari.properties override                               |

Above configuration files can safely be edited, modifications will not be replaced when the RPM packages are updated.

### Log files

| Log file                  | Description            |
|---------------------------|------------------------|
| /var/log/jetty/oskari.log | Oskari application log |
| /var/log/jetty/access.log | Web server access log  |

Service standard output can also be read from journal:
```bash
journalctl -u oskari-jetty
```

## Packaging Oskari frontend

A sample RPM Spec file for packaging Oskari frontend is also included. By default, this is configured to use the Apache HTTPD webserver.
Another server software (e.g nginx) can be used by adjusting the variables `basedir` and `webserverpkg` in `packages/rpm/SPECS/oskari-frontend.spec`

### Build instructions

If you have the oskari-frontend and a custom application (community) repository (say myapp-frontend) setup as follows:

oskari-frontend  
myapp-frontend

And the webpack build has been executed successfully, an rpm package can be created as follows.
A vanilla frontend build can naturally be packaged by creating the source tarball accordingly.

```bash
tar cvf oskari-frontend.tar -C oskari-frontend bundles libraries resources
tar rvf oskari-frontend.tar -C myapp-frontend dist bundles
gzip -f oskari-frontend.tar
     
cp PATH_TO_FRONTEND_REPOS/oskari-frontend-tar.gz packages/rpm/SOURCES/

cd packages/rpm
rpmbuild -bb SPECS/oskari-frontend.spec --define "_topdir $(pwd)" --define "ver VERSION" --define "rel RELEASE"
```

