Name:           maven-native
Version:        1.0.alpha.7
Release:        1%{?dist}
Summary:        Maven plugin for native compilation tasks

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://mojo.codehaus.org/maven-native/native-maven-plugin/
# tar creation instructions
# svn export http://svn.codehaus.org/mojo/tags/maven-native-1.0-alpha-7/
# tar cfz maven-native-1.0.alpha.7.tar.gz maven-native-1.0-alpha-7
Source0:        %{name}-%{version}.tar.gz
Patch0:         mnp-fixes-for-F18-compile.patch
# remove testng dep (tests are skipped)
BuildArch:      noarch

# basic deps
BuildRequires:  java-devel
BuildRequires:  jpackage-utils

# maven-* build deps
BuildRequires:  maven-shared
BuildRequires:  maven-artifact-resolver
BuildRequires:  maven-model
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-project

# other build deps
BuildRequires:  backport-util-concurrent
BuildRequires:  bcel
BuildRequires:  apache-commons-lang
BuildRequires:  plexus-archiver
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils

Requires:       java
Requires:       jpackage-utils
Requires:       maven
Requires:       maven-shared

%description
Use this plugin to compile C and C++ source under Maven 2
or higher with compilers such as gcc, msvc, gcj, etc.


%package javadoc
Summary:        Javadocs for %{name}
Group:          Documentation
Requires:       jpackage-utils
BuildArch:      noarch

%description javadoc
This package contains the API documentation for %{name}.


%prep
%setup -q -n maven-native-1.0-alpha-7
%patch0 -p2

# fix EOL
sed -i 's/\r//' LICENSE.txt

%build
mvn-rpmbuild -Dmaven.test.skip=true install javadoc:aggregate

%install
mkdir -p $RPM_BUILD_ROOT%{_javadir}
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}

# jar
install -Dp -m 644 %{name}-api/target/%{name}-api-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/api.jar
install -Dp -m 644 %{name}-components/%{name}-msvc/target/%{name}-msvc-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/msvc.jar
install -Dp -m 644 %{name}-components/%{name}-generic-c/target/%{name}-generic-c-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/generic-c.jar
install -Dp -m 644 %{name}-components/%{name}-manager/target/%{name}-manager-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/manager.jar
install -Dp -m 644 %{name}-components/%{name}-bcc/target/%{name}-bcc-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/bcc.jar
install -Dp -m 644 %{name}-components/%{name}-javah/target/%{name}-javah-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/javah.jar
# naming reversed for some reason
install -Dp -m 644 native-maven-plugin/target/native-maven-plugin-1.0-alpha-7.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/plugin.jar

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}.pom
install -pm 644 %{name}-api/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-api.pom
install -pm 644 %{name}-components/%{name}-msvc/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-msvc.pom
install -pm 644 %{name}-components/%{name}-generic-c/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-generic-c.pom
install -pm 644 %{name}-components/%{name}-manager/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-manager.pom
install -pm 644 %{name}-components/%{name}-bcc/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-bcc.pom
install -pm 644 %{name}-components/%{name}-javah/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-javah.pom
install -pm 644 native-maven-plugin/pom.xml  $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-plugin.pom

%add_maven_depmap JPP.%{name}.pom
%add_maven_depmap JPP.%{name}-api.pom %{name}/api.jar
%add_maven_depmap JPP.%{name}-msvc.pom %{name}/msvc.jar
%add_maven_depmap JPP.%{name}-generic-c.pom %{name}/generic-c.jar
%add_maven_depmap JPP.%{name}-manager.pom %{name}/manager.jar
%add_maven_depmap JPP.%{name}-bcc.pom %{name}/bcc.jar
%add_maven_depmap JPP.%{name}-javah.pom %{name}/javah.jar
%add_maven_depmap JPP.%{name}-plugin.pom %{name}/plugin.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%doc LICENSE.txt
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

%changelog
* Fri Mar 29 2013 Pete MacKinnon <pmackinn@redhat.com> -1
- Initial packaging
