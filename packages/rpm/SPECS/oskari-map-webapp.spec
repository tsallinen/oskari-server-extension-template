%global jettyuser jetty
%global jettygroup jetty
%global servicedir jetty
%global jetty_webapps %{_sharedstatedir}/%{servicedir}/webapps
%global webapp_name oskari-map

%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

Name:           oskari-map-webapp
Version:        %{ver}
Release:        %{rel}%{?dist}
Packager:       National Land Survey of Finland
URL:            http://oskari.org
Group:          Applications/Internet
License:        MIT
BuildArch:      noarch
Summary:        Oskari Map webapp
Requires:       oskari-jetty
Requires:       java => 1.8
Autoreq:        0
Autoprov:       0

%description
Oskari Map webapp

%define src %{_topdir}/../..

%prep
rm -rf %{name}
mkdir %{name}
cd %{name}
unzip %{src}/webapp-map/target/oskari-map.war

%build

%install
%{__install} -m 755 -d %{buildroot}%{jetty_webapps}/%{webapp_name}
cp -a %{name}/* %{buildroot}%{jetty_webapps}/%{webapp_name}/
%{__install} -m 755 -d %{buildroot}%{_sharedstatedir}/%{servicedir}/resources
touch %{buildroot}%{_sharedstatedir}/%{servicedir}/resources/oskari-ext.properties

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%{jetty_webapps}/%{webapp_name}
%config(noreplace) %{_sharedstatedir}/%{servicedir}/resources/oskari-ext.properties

%changelog
