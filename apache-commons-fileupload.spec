%global base_name       fileupload
%global short_name      commons-%{base_name}

%{?scl:%scl_package apache-%{short_name}}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

%if 0%{?rhel}

%if 0%{?rhel} <= 6
  # EL 6
  %global custom_release 60
%else
  # EL 7
  %global custom_release 70
%endif

%else

%global custom_release 1

%endif

Name:             %{?scl_prefix}apache-%{short_name}
Version:          1.3
Release:          %{custom_release}.1%{?dist}
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Libraries
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:        noarch

Patch1:           CVE-2013-2186-commons-fileupload.patch
# Backported from upstream revision 1565143
Patch2:           %{pkg_name}-CVE-2014-0050.patch

BuildRequires:    %{?scl_prefix_maven}maven-local
BuildRequires:    %{?scl_prefix_java_common}junit >= 0:3.8.1
BuildRequires:    %{?scl_prefix_java_common}mvn(javax.servlet:servlet-api)
BuildRequires:    %{?scl_prefix_java_common}apache-commons-io
BuildRequires:    %{?scl_prefix_maven}maven-antrun-plugin
BuildRequires:    %{?scl_prefix_maven}maven-assembly-plugin
BuildRequires:    %{?scl_prefix_maven}maven-compiler-plugin
BuildRequires:    %{?scl_prefix_maven}maven-doxia-sitetools
BuildRequires:    %{?scl_prefix_maven}maven-install-plugin
BuildRequires:    %{?scl_prefix_maven}maven-jar-plugin
BuildRequires:    %{?scl_prefix_maven}maven-javadoc-plugin
BuildRequires:    %{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:    %{?scl_prefix_maven}maven-release-plugin
BuildRequires:    %{?scl_prefix_maven}maven-resources-plugin
BuildRequires:    %{?scl_prefix_maven}buildnumber-maven-plugin
%if 0%{?fedora}
BuildRequires:    portlet-2.0-api
%endif

%if 0%{?fedora}
Requires:         portlet-2.0-api
%endif

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package javadoc
Summary:          API documentation for %{name}
Group:            Documentation

%description javadoc
This package contains the API documentation for %{name}.

# -----------------------------------------------------------------------------

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{short_name}-%{version}-src
%patch2 -p1
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

%if 0%{?fedora}
# fix gId
sed -i "s|<groupId>portlet-api</groupId>|<groupId>javax.portlet</groupId>|" pom.xml
%else
# Non-Fedora: remove portlet stuff
%pom_remove_dep portlet-api:portlet-api
%pom_xpath_remove pom:properties/pom:commons.osgi.import
%pom_xpath_remove pom:properties/pom:commons.osgi.dynamicImport
rm -r src/main/java/org/apache/commons/fileupload/portlet
rm src/test/java/org/apache/commons/fileupload/*Portlet*
%endif
pushd src/main
%patch1 -p1
popd
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# fix build with generics support
# tests fail to compile because they use an obsolete version of servlet API (2.4)
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}

%files javadoc -f .mfiles-javadoc

%changelog
* Fri Jun 24 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.3-1
- Initial package.
