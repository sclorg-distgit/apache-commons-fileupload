%global base_name       fileupload
%global short_name      commons-%{base_name}

%{?scl:%scl_package apache-%{short_name}}
%{!?scl:%global pkg_name %{name}}

# Use java common's requires/provides generator
%{?java_common_find_provides_and_requires}

# Exclude generation of osgi() style provides, since they are not
# SCL-namespaced and may conflict with base RHEL packages.
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1045442
%global __provides_exclude ^osgi(.*)$

Name:             %{?scl_prefix}apache-%{short_name}
Version:          1.3
# Release should be higher than el6 builds. Use convention
# 60.X where X is an increasing int. 60 for rhel-6. We use
# 70.X for rhel-7. For some reason we cannot rely on the
# dist tag.
Release:          70.5%{?dist}
Summary:          This package provides an api to work with html file upload
License:          ASL 2.0
Group:            Development/Libraries
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:        noarch

Patch1:           CVE-2013-2186-commons-fileupload.patch
# Backported from upstream revision 1565143
Patch2:           %{pkg_name}-CVE-2014-0050.patch

BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    %{?scl_prefix_java_common}maven-local
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

Requires:         java >= 1:1.6.0
%if 0%{?fedora}
Requires:         portlet-2.0-api
%endif
# Make sure we depend on the scl-runtime package
%{?scl:Requires: %scl_runtime}

%description
The javax.servlet package lacks support for rfc 1867, html file
upload.  This package provides a simple to use api for working with
such data.  The scope of this package is to create a package of Java
utility classes to read multipart/form-data within a
javax.servlet.http.HttpServletRequest

%package javadoc
Summary:          API documentation for %{name}
Group:            Documentation
%{?scl:Requires: %scl_runtime}

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
* Wed Mar 30 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.3-70.5
- Own in collection directory.
- Resolves: RHBZ#1317970

* Wed Jan 27 2016 Severin Gehwolf <sgehwolf@redhat.com> 1.3-70.4
- Rebuild for RHSCL 2.2.

* Mon Jan 19 2015 Severin Gehwolf <sgehwolf@redhat.com> 1.3-70.3
- Require java common's libs for building instead of maven's
  collection libs.

* Thu Dec 18 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.3-70.2
- Use maven30 collection for building.
- Use java common's requires/provides generators.

* Mon Jun 23 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.3-70.1
- Add requires for thermostat1-runtime package.

* Tue Feb 18 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.3-12
- Add backported upstream patch to fix DoS vulnerability
- Resolves: RHBZ#1064677

* Mon Jan 27 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.3-11
- Own scl-ized apache-commons-fileupload directory in javadir.
- Resolves: RHBZ#1057169

* Mon Jan 20 2014 Severin Gehwolf <sgehwolf@redhat.com> 1.3-10
- Apply patch for CVE-2013-2186.
- Resolves: RHBZ#1055528

* Fri Dec 20 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-9
- Don't generate osgi() style provides.
- Fix bogus changelog date.
- Resolves RHBZ#1045442

* Wed Nov 27 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-8
- Properly enable SCL.

* Wed Nov 06 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-7
- Source xmvn configuration prior building/installing.

* Wed Nov 06 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-6
- Use xmvn.

* Tue Sep 17 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-5
- Add BR buildnumber-maven-plugin.

* Wed Aug 28 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-4
- SCL-ize package.

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.3-3
- Remove unneeded BR: maven-idea-plugin

* Thu Apr 18 2013 Severin Gehwolf <sgehwolf@redhat.com> 1.3-2
- Use pom macros over patch.
- Remove surefire maven plugin since tests are skipped anyway.

* Thu Mar 28 2013 Michal Srb <msrb@redhat.com> - 1.3-1
- Update to upstream version 1.3

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.2-11
- Disable tests (they use obsolete servlet API 2.4)
- Resolves: rhbz#913878

* Thu Feb 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.2-10
- Add missing BR: maven-local

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Severin Gehwolf <sgehwolf@redhat.com> 1.2.2-8
- Conditionally build portlet-2.0-api support in Fedora only

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.2-6
- Fix up patches to apply, cleanup spec old coments
- Fix surefire plugin dependency to use new name

* Tue May 29 2012 gil cattaneo <puntogil@libero.it> 1.2.2-5
- Add portlet-2.0-api support (required by springframework).

* Fri Mar  2 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> 1.2.2-4
- Fix build and update to latest guidelines

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Chris Spike <chris.spike@arcor.de> 1.2.2-1
- Updated to 1.2.2
- Fixed License tag
- tomcat5 -> tomcat6 BRs/Rs
- Fixed wrong EOL encodings

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-4
- Add license to javadoc subpackage

* Thu May 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-3
- Added Requires on jpackage-utils for javadoc

* Thu May 20 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2.1-2
- Rename package (jakarta-commons-fileupload->apache-commons-fileupload)
- Re-did whole spec file

* Wed Jan  6 2010 Mary Ellen Foster <mefoster at gmail.com> - 1:1.2.1-1
- Update to newest version; include Maven metadata

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-9.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0-8.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:1.0-7.3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0-7jpp.2
- Autorebuild for GCC 4.3

* Tue Apr 17 2007 Permaine Cheung <pcheung@redhat.com> - 1:1.0-6jpp.2
- Update spec file as per fedora review

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> - 1:1.0-6jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 1.0-5jpp_3fc
- Requires(post/postun): coreutils

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 1:1.0-5jpp_2fc
- Rebuilt

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> - 1:1.0-5jpp_1fc
- Added conditional native compilation.

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 1:1.0-4jpp
- First JPP 1.7 build

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> - 1:1.0-3jpp
- Patch to build with servletapi5
- Add missing dependency on ant-junit

* Mon Aug 23 2004 Randy Watler <rwatler at finali.com> - 1:1.0-2jpp
- Rebuild with ant-1.6.2

* Sat Jun 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-1jpp
- Update to 1.0.
- Add Epochs to dependencies.
- Nuke beanutils dependency.
- Versionless javadoc dir symlinks.

* Tue Mar 25 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> - 1:1.0-0.beta1.4jpp
- for jpackage-utils 1.5

* Mon Mar 10 2003 Henri Gomez <hgomez@users.sourceforge.net> - 1:1.0-0.beta1.3jpp
- rebuild with correct ant (avoid corrupted archive)

* Fri Mar 07 2003 Henri Gomez <hgomez@users.sourceforge.net> - 1:1.0-0.beta1.2jpp
- replace servlet23 requirement by servlet4api

* Wed Feb 26 2003 Ville Skyttä <ville.skytta at iki.fi> - 1:1.0-0.beta1.1jpp
- Update to 1.0 beta 1 (no code changes from cvs20030115).
- Fix requirements.

* Wed Jan 15 2003 Henri Gomez <hgomez@users.sourceforge.net> 1.0-1jpp
- 1.0 (cvs 20030115)
- first jPackage release
