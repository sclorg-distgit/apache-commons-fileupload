%global pkg_name apache-commons-fileupload
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}

Name:             %{?scl_prefix}%{pkg_name}
Version:          1.3.2
Release:          1%{?dist}
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Libraries
URL:              http://commons.apache.org/fileupload
Source0:          http://www.apache.org/dist/commons/fileupload/source/commons-fileupload-%{version}-src.tar.gz
BuildArch:        noarch

BuildRequires:    %{?scl_prefix}mvn(commons-io:commons-io)
BuildRequires:    %{?scl_prefix}mvn(javax.servlet:servlet-api)
BuildRequires:    %{?scl_prefix}mvn(junit:junit)
BuildRequires:    %{?scl_prefix_maven}mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:    %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:    %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-release-plugin)


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


%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n commons-fileupload-%{version}-src
sed -i 's/\r//' LICENSE.txt
sed -i 's/\r//' NOTICE.txt

# remove portlet stuff
%pom_remove_dep portlet-api:portlet-api
%pom_xpath_remove pom:properties/pom:commons.osgi.import
%pom_xpath_remove pom:properties/pom:commons.osgi.dynamicImport
rm -r src/main/java/org/apache/commons/fileupload/portlet

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
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Tue Jul 26 2016 Michael Simacek <msimacek@redhat.com> - 1.3.2-1
- Prepare for rh-java-common inclusion
- Update to version 1.3.2

* Fri Jun 24 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.3-1
- Initial package.
