# oskari-server-extension-template

This is a template for extending oskari-server functionality using Maven.

Modify oskari-ext.properties:

    # replace 'sample' with 'myapp'
    db.additional.modules=myplaces, analysis, userlayer, myapp
    
    # default view is the first appsetup
    view.default=1
    
    # publish template is the second appsetup
    view.template.publish=2

    # make myplaces etc baselayers have the correct projection for initial setup:
    oskari.native.srs=EPSG:3067

To enable end-user registration configure these (more information at http://oskari.org/documentation/features/usermanagement):

    allow.registration=true
    oskari.email.sender=<sender@domain.com>
    oskari.email.host=<smtp.domain.com>

If you would like to have a non-admin user you can add these lines to app-resouces/src/main/resources/sql/initial-users.sql:

    -- add user;
    INSERT INTO oskari_users(user_name, first_name, last_name, uuid) VALUES('user', 'Oskari', 'Olematon', 'fdsa-fdsa-fdsa-fdsa-fdsa');
    
    -- add role to user;
    INSERT INTO oskari_role_oskari_user(user_id, role_id) VALUES((SELECT id FROM oskari_users WHERE user_name = 'user'), (SELECT id FROM oskari_roles WHERE name = 'User'));
    
    -- add credentials user/user for non-admin user;
    INSERT INTO oskari_jaas_users(login, password) VALUES('user', 'MD5:ee11cbb19052e40b07aac0ca060c23ee');

Compile with:

    mvn clean install
    
Replace oskari-map.war under {jetty.home}/webapps/ with the one created under webapp-map/target 

# Reporting issues

All Oskari-related issues should be reported here: https://github.com/oskariorg/oskari-docs/issues
