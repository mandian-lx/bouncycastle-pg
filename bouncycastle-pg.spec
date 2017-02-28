%{?_javapackages_macros:%_javapackages_macros}

%global ver 1.54
%global archivever  jdk15on-%(echo %{ver}|sed 's|\\\.||')

Name:          bouncycastle-pg
Version:       %{ver}
Release:       1
Summary:       Bouncy Castle OpenPGP API
# modified BZIP2 library org/bouncycastle/apache/bzip2 ASL 2.0
License:       ASL 2.0 and MIT
URL:           http://www.bouncycastle.org/

# Source tarball contains everything except test suite rousources
Source0:       http://www.bouncycastle.org/download/bcpg-%{archivever}.tar.gz
# Test suite resources are found in this jar
Source1:       http://www.bouncycastle.org/download/bctest-%{archivever}.jar

Source2:       http://repo2.maven.org/maven2/org/bouncycastle/bcpg-jdk15on/%{version}/bcpg-jdk15on-%{version}.pom
Source3:       bouncycastle-pg-build.xml
Source4:       bouncycastle-pg-OSGi.bnd
Patch0:        %{name}-1.54-fix_missing_bnd.patch

BuildRequires: ant
BuildRequires: ant-junit
BuildRequires: aqute-bnd
BuildRequires: jpackage-utils
BuildRequires: junit
BuildRequires: mvn(org.bouncycastle:bcprov-jdk15on) = %{version}
Requires:      mvn(org.bouncycastle:bcprov-jdk15on) = %{version}

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

# Unzip source and test suite resources
mkdir -p src/java src/test
unzip -qq src.zip -d src/java
unzip -qq %{SOURCE1} 'org/bouncycastle/openpgp/**' -x '**.class' -d src/java

mkdir -p src/test/org/bouncycastle/openpgp/examples
mv src/java/org/bouncycastle/openpgp/test \
  src/test/org/bouncycastle/openpgp/
mv src/java/org/bouncycastle/openpgp/examples/test \
  src/test/org/bouncycastle/openpgp/examples/

# Remove provided binaries and apidocs
find . -type f -name "*.class" -exec rm -f {} \;
find . -type f -name "*.jar" -exec rm -f {} \;
rm -rf docs/* javadocs/*

cp -p %{SOURCE3} build.xml
cp -p %{SOURCE4} bcpg.bnd
sed -i "s|@VERSION@|%{version}|" build.xml bcpg.bnd

# fix missing /usr/bin/bnd
%patch0 -p1 -b .orig

# this test fails: source encoding error
rm src/test/org/bouncycastle/openpgp/test/PGPUnicodeTest.java
sed -i "s|suite.addTestSuite(PGPUnicodeTest.class);|//&|" \
  src/test/org/bouncycastle/openpgp/test/AllTests.java

%build
mkdir lib
build-jar-repository -s -p lib bcprov junit ant/ant-junit aqute-bnd
ant -Dbc.test.data.home=$(pwd)/src/test jar javadoc
java -jar $(build-classpath aqute-bnd) wrap -properties bcpg.bnd build/bcpg.jar
mv bcpg.bar build/bcpg.jar

%install
%mvn_file org.bouncycastle:bcpg-jdk15on bcpg
%mvn_alias org.bouncycastle:bcpg-jdk15on org.bouncycastle:bcpg-jdk16 org.bouncycastle:bcpg-jdk15
%mvn_artifact %{SOURCE2} build/bcpg.jar
%mvn_install -J build/apidocs

%files -f .mfiles
%doc CONTRIBUTORS.html index.html
%doc LICENSE.html

%files javadoc -f .mfiles-javadoc
%doc LICENSE.html

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Apr 07 2016 Mat Booth <mat.booth@redhat.com> - 1.54-1
- Update to 1.54
- Fix most of the test failures

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.52-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 17 2015 gil cattaneo <puntogil@libero.it> 1.52-8
- remove the OSGi deprecated entry in bnd properties file

* Thu Jul 16 2015 gil cattaneo <puntogil@libero.it> 1.52-7
- add BR aqute-bndlib
- disable doclint

* Thu Jul 16 2015 Michael Simacek <msimacek@redhat.com> - 1.52-6
- Use aqute-bnd-2.4.1

* Tue Jun 23 2015 gil cattaneo <puntogil@libero.it> 1.52-5
- dropped the Export/Import-Package lists in the bnd properties file

* Thu Jun 18 2015 gil cattaneo <puntogil@libero.it> 1.52-4
- fix OSGi export

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.52-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 gil cattaneo <puntogil@libero.it> 1.52-2
- Use javapackages macros

* Wed Apr 22 2015 Alexander Kurtakov <akurtako@redhat.com> 1.52-1
- Update to 1.52.
- Bump source/target to 1.6 as 1.5 is target for removal in Java 9

* Thu Jan 29 2015 gil cattaneo <puntogil@libero.it> 1.50-6
- install license file in main package

* Thu Jan 29 2015 gil cattaneo <puntogil@libero.it> 1.50-5
- introduce license macro

* Wed Oct 22 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.50-4
- Add alias for org.bouncycastle:bcpg-jdk15

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Michal Srb <msrb@redhat.com> - 1.50-2
- Fix OSGi metadata

* Mon Feb 24 2014 Michal Srb <msrb@redhat.com> - 1.50-1
- Update to upstream version 1.50
- Switch to java-headless

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
