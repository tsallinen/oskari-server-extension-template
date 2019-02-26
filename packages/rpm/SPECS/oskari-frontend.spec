#Apache HTTPD
%global basedir /var/www/html/Oskari
%global webserverpkg httpd

# Uncomment these for nginx
#%global basedir /usr/share/nginx/html/Oskari
#%global webserverpkg nginx

Name:           oskari-frontend
Version:        %{ver}
Release:        %{rel}
License:        MIT
Summary:        Oskari frontend
BuildArch:      noarch
Source0:        oskari-frontend.tar.gz

Requires:       %{webserverpkg}
%description

%prep
%setup -q -c -n oskari-frontend

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{basedir}
cp -pr ./* %{buildroot}%{basedir}/

%files
%defattr(-,root,root,-)
%dir %{basedir}
%{basedir}/*

%changelog
