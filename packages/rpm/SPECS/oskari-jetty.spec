%global servicename oskari-jetty
%global jettyuser jetty
%global jettygroup jetty
%global servicedir jetty

%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

Name:           oskari-jetty
Version:        %{ver}
Release:        %{rel}%{?dist}
Summary:        Oskari Server (Jetty)
Packager:       National Land Survey of Finland
Group:          System Environment/Daemons
License:        Apache and Eclipse
URL:            http://oskari.org
Source1:        %{servicename}.service
Source2:        %{servicename}-sysconfig
Source3:        oskari-jetty.logrotate
Source4:        db.properties
Source5:        log4j.properties
Source6:        logback-access.xml
BuildArch:      noarch
BuildRequires:  systemd
Requires:       java => 1.8

Autoreq:        0
Autoprov:       0

%define src %{_topdir}/../..

%description
Embedded Jetty Server for Oskari.

%prep
rm -rf %{name}
mkdir %{name}
cd %{name}
unzip %{src}/oskari-jetty/target/oskari-jetty-deps.zip

%build

%pre
getent group %{jettygroup} >/dev/null || groupadd -r %{jettygroup}
getent passwd %{jettyuser} >/dev/null || \
useradd -r -g %{jettygroup} -s /sbin/nologin -d /usr/share/%{servicename} \
    -c "Jetty" %{jettyuser} || :

%post
%systemd_post %{servicename}.service

%preun
%systemd_preun %{servicename}.service

%postun
%systemd_postun_with_restart %{servicename}.service

%install
%{__install} -m 755 -d %{buildroot}%{_unitdir}/
%{__install} -m 755 -d %{buildroot}%{_prefix}/share/%{servicedir}/lib
%{__install} -m 755 -d %{buildroot}%{_localstatedir}/log/%{servicedir}
%{__install} -m 755 -d %{buildroot}%{_sharedstatedir}/%{servicedir}/webapps
%{__install} -m 755 -d %{buildroot}%{_sharedstatedir}/%{servicedir}/resources
%{__install} -m 755 -d %{buildroot}/%{_sysconfdir}/sysconfig

%{__install} -m 755 -d %{buildroot}%{_localstatedir}/cache/%{servicedir}
%{__install} -m 755 -d %{buildroot}%{_localstatedir}/cache/%{servicedir}/work
%{__install} -m 755 -d %{buildroot}%{_localstatedir}/cache/%{servicedir}/temp

cp -a %{name}/* %{buildroot}%{_prefix}/share/%{servicedir}/lib/

%{__install} -m 644 %{SOURCE4} %{buildroot}%{_sharedstatedir}/%{servicedir}/resources/
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_sharedstatedir}/%{servicedir}/resources/
%{__install} -m 644 %{SOURCE6} %{buildroot}%{_sharedstatedir}/%{servicedir}/resources/

%{__install} -m 755 -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -c -m 755 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/oskari-jetty

ln -s %{_sharedstatedir}/%{servicedir}/resources %{buildroot}%{_prefix}/share/%{servicedir}/resources
ln -s %{_sharedstatedir}/%{servicedir}/webapps %{buildroot}%{_prefix}/share/%{servicedir}/webapps
ln -s %{_localstatedir}/cache/%{servicedir}/temp %{buildroot}%{_prefix}/share/%{servicedir}/temp
ln -s %{_localstatedir}/cache/%{servicedir}/work %{buildroot}%{_prefix}/share/%{servicedir}/work

%{__install} -c -m 755 %{SOURCE1} %{buildroot}%{_unitdir}
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{servicename}

%clean
rm -rf %{buildroot}

%files
%dir %attr(775, root, %{jettygroup}) %{_prefix}/share/%{servicedir}
%dir %attr(775, root, %{jettygroup}) %{_prefix}/share/%{servicedir}/lib
%{_prefix}/share/%{servicedir}/resources
%{_prefix}/share/%{servicedir}/temp
%{_prefix}/share/%{servicedir}/webapps
%{_prefix}/share/%{servicedir}/work

%attr(644, root, root) /usr/share/%{servicedir}/lib/*.jar
%defattr(-,root,root,-)

%attr(775, %{jettyuser}, %{jettygroup}) %{_localstatedir}/log/%{servicedir}
%dir %attr(755, root,root) %{_sharedstatedir}/%{servicedir}
%dir %attr(775, %{jettyuser}, %{jettygroup}) %{_sharedstatedir}/%{servicedir}/webapps

%{_unitdir}/%{servicename}.service

%config(noreplace) %{_sysconfdir}/sysconfig/%{servicename}
%config(noreplace) %{_sharedstatedir}/%{servicedir}/resources/db.properties
%config(noreplace) %{_sharedstatedir}/%{servicedir}/resources/log4j.properties
%config(noreplace) %{_sharedstatedir}/%{servicedir}/resources/logback-access.xml

%dir %attr(775, %{jettyuser}, %{jettygroup}) %{_localstatedir}/cache/%{servicedir}
%dir %attr(775, %{jettyuser}, %{jettygroup}) %{_localstatedir}/cache/%{servicedir}/temp
%dir %attr(775, %{jettyuser}, %{jettygroup}) %{_localstatedir}/cache/%{servicedir}/work

%config(noreplace) %{_sysconfdir}/logrotate.d/oskari-jetty

%changelog
