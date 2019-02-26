%global jettyuser jetty
%global jettygroup jetty
%global servicedir jetty
%global jetty_webapps %{_sharedstatedir}/%{servicedir}/webapps


%define __spec_install_post %{nil}
%define debug_package %{nil}
%define __os_install_post %{_dbpath}/brp-compress

Name:           oskari-transport-webapp
Version:        %{ver}
Release:        %{rel}%{?dist}
Packager:       National Land Survey of Finland
URL:            http://oskari.org
Group:          Applications/Internet
License:        MIT
BuildArch:      noarch
Summary:        Oskari Transport webapp
Requires:       oskari-jetty
Requires:       java => 1.8
Autoreq:        0
Autoprov:       0

%description
Oskari Transport webapp

%define src %{_topdir}/../..

%prep
rm -rf %{name}
mkdir %{name}
cd %{name}
unzip %{src}/webapp-transport/target/transport.war

%build

%install
%{__install} -m 755 -d %{buildroot}%{jetty_webapps}/transport
cp -a %{name}/* %{buildroot}%{jetty_webapps}/transport/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%{jetty_webapps}/transport

%changelog
