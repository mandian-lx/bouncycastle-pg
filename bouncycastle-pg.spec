%{?_javapackages_macros:%_javapackages_macros}
%global ver 146
%global archivever  jdk16-%(echo %{ver}|sed 's|\\\.||')
Name:          bouncycastle-pg
Version:       1.46
Release:       10%{?dist}
Summary:       Bouncy Castle OpenPGP API
Group:         Development/Libraries
# modified BZIP2 library org/bouncycastle/apache/bzip2 ASL 2.0
License:       ASL 2.0 and MIT
URL:           http://www.bouncycastle.org/
Source0:       http://www.bouncycastle.org/download/bcpg-%{archivever}.tar.gz
Source1:       http://repo2.maven.org/maven2/org/bouncycastle/bcpg-jdk16/%{version}/bcpg-jdk16-%{version}.pom
Source2:       bouncycastle-pg-%{version}-01-build.xml
Source3:       bouncycastle-pg-%{version}-OSGi.bnd

BuildRequires: java-devel
BuildRequires: jpackage-utils

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: aqute-bnd
BuildRequires: junit

BuildRequires: bouncycastle = %{version}

Requires:      bouncycastle = %{version}

Requires:      java
Requires:      jpackage-utils
BuildArch:     noarch

%description
The Bouncy Castle Java API for handling the OpenPGP protocol. This
jar contains the OpenPGP API for JDK 1.6. The APIs can be used in 
conjunction with a JCE/JCA provider such as the one provided with the
Bouncy Castle Cryptography APIs.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n bcpg-%{archivever}
# fixing incomplete source directory structure
mkdir -p src/java src/test
unzip -qq src.zip -d src/java

mkdir -p src/test/org/bouncycastle/openpgp/test
mv src/java/org/bouncycastle/openpgp/test/* \
  src/test/org/bouncycastle/openpgp/test
mkdir -p src/test/org/bouncycastle/openpgp/examples/test
mv src/java/org/bouncycastle/openpgp/examples/test/* \
  src/test/org/bouncycastle/openpgp/examples/test

# Remove provided binaries and apidocs
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;
rm -rf docs/*

cp -p %{SOURCE2} build.xml
cp -p %{SOURCE3} bcpg.bnd

# this test fails: bc.test.data.home property not set
rm src/test/org/bouncycastle/openpgp/test/DSA2Test.java
sed -i "s|suite.addTestSuite(DSA2Test.class);|//suite.addTestSuite(DSA2Test.class);|" \
  src/test/org/bouncycastle/openpgp/test/AllTests.java

%build

%ant jar javadoc

%install

mkdir -p %{buildroot}%{_javadir}
install -pm 644 build/bcpg.jar %{buildroot}%{_javadir}/bcpg.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-bcpg.pom
%add_maven_depmap JPP-bcpg.pom bcpg.jar

%files -f .mfiles
%doc *.html

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.html

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 10 2012 gil cattaneo <puntogil@libero.it> 1.46-7
- change SOURCE0 see rhbz#806262

* Tue May 08 2012 gil cattaneo <puntogil@libero.it> 1.46-6
- used %%global instead %%define
- removed the checks for fedora version
- removed requirement from javadoc subpackage

* Wed May 02 2012 gil cattaneo <puntogil@libero.it> 1.46-5
- fix BRs for fedora > f16
- add BR ant-junit

* Wed May 02 2012 gil cattaneo <puntogil@libero.it> 1.46-4
- rebuilt with ant and aqute-bndlib 0.0.363 support
- removed BR zip

* Sun Apr 15 2012 gil cattaneo <puntogil@libero.it> 1.46-3
- removed BR unzip

* Tue Apr 10 2012 gil cattaneo <puntogil@libero.it> 1.46-2
- add BR zip

* Sun Mar 25 2012 gil cattaneo <puntogil@libero.it> 1.46-1
- initial rpm