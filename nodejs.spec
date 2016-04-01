%define   _base node
%define   _dist_ver %(sh /usr/lib/rpm/redhat/dist.sh)
%define   _dist_name %(cat /etc/redhat-release | cut -d " " -f 1)
%define   _includedir %{_prefix}/include
%define   _bindir %{_prefix}/bin
%define   _libdir %{_prefix}/lib

%if "%{_dist_ver}" == ".el5"
%define   _datarootdir%{_datadir}
%endif

%global tapsetroot %{_prefix}/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}

Name:          %{_base}js
Version:       4.4.2
Release:       1%{?dist}
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
Packager:      Kazuhisa Hara <kazuhisya@gmail.com>
Group:         Development/Libraries
License:       MIT License
URL:           https://nodejs.org
Source0:       %{url}/dist/v%{version}/%{_base}-v%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix:        /usr
BuildRequires: redhat-rpm-config
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel
BuildRequires: gzip
BuildRequires: python

%if "%{_dist_ver}" == ".el7" || "%{_dist_name}" == "Fedora"
BuildRequires: libicu-devel
Requires: libicu
%endif

%if "%{_dist_ver}" == ".el5"
# require EPEL
BuildRequires: python27
%endif

Patch0: node-js.centos5.configure.patch
Patch1: node-js.centos5.gyp.patch
Patch2: node-js.centos5.icu.patch
Patch3: node-js.system-icu.patch

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package binary
Summary:       Node.js build binary tarballs
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description binary
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package npm
Summary:       Node Packaged Modules
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org
Obsoletes:     npm
Provides:      npm
Requires:      nodejs

%description npm
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package devel
Summary:       Header files for %{name}
Group:         Development/Libraries
Requires:      %{name}

%description devel
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version}
%setup -q -n %{_base}-v%{version}

%if "%{_dist_ver}" == ".el5"
%patch0 -p1
%patch1 -p1
%patch2 -p1
%endif

%if "%{_dist_ver}" == ".el7" || "%{_dist_name}" == "Fedora"
%patch3 -p1
%endif

%build
%if "%{_dist_ver}" == ".el5"
export PYTHON=python2.7
%endif

%define _node_arch %{nil}
%ifarch x86_64
%define _node_arch x64
%endif
%ifarch i386 i686
%define _node_arch x86
%endif
if [ -z %{_node_arch} ];then
  echo "bad arch"
  exit 1
fi

./configure \
    --shared-openssl \
    --shared-openssl-includes=%{_includedir} \
    --shared-zlib \
    --shared-zlib-includes=%{_includedir}
make binary %{?_smp_mflags}

pushd $RPM_SOURCE_DIR
mv $RPM_BUILD_DIR/%{_base}-v%{version}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz .
rm -rf %{_base}-v%{version}
tar zxvf %{_base}-v%{version}-linux-%{_node_arch}.tar.gz
popd

%install
rm -rf $RPM_BUILD_ROOT
mkdir  -p $RPM_BUILD_ROOT%{_prefix}
cp -Rp $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}/* $RPM_BUILD_ROOT%{_prefix}/
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{_base}-v%{version}/

for file in CHANGELOG.md LICENSE README.md ; do
    mv $RPM_BUILD_ROOT%{_prefix}/$file $RPM_BUILD_ROOT%{_defaultdocdir}/%{_base}-v%{version}/
done
mv $RPM_BUILD_ROOT%{_defaultdocdir}/node/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{_base}-v%{version}/
rm -rf $RPM_BUILD_ROOT%{_defaultdocdir}/node
mkdir -p $RPM_BUILD_ROOT%{_datarootdir}/%{_base}js
mv $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz $RPM_BUILD_ROOT%{_datarootdir}/%{_base}js/

# prefix all manpages with "npm-"
pushd $RPM_BUILD_ROOT%{_libdir}/node_modules/npm/man/
for dir in *; do
    mkdir -p $RPM_BUILD_ROOT%{_mandir}/$dir
    pushd $dir
    for page in *; do
        if [[ $page != npm* ]]; then
        mv $page npm-$page
    fi
    done
    popd
    cp $dir/* $RPM_BUILD_ROOT%{_mandir}/$dir
done
popd

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}

%files
%defattr(-,root,root,-)
%{_defaultdocdir}/%{_base}-v%{version}
%defattr(755,root,root)
%{_bindir}/node

%doc
%{_mandir}/man1/node.1.gz

%files binary
%defattr(-,root,root,-)
%{_datarootdir}/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%files npm
%defattr(-,root,root,-)
%{_libdir}/node_modules/npm
%{_bindir}/npm

%doc
%{_mandir}/man1/npm*
%{_mandir}/man3
%{_mandir}/man5
%{_mandir}/man7

%files devel
%{_includedir}/node/
%{tapsetroot}

%changelog
* Fri Apr  1 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.4.2-1
- Updated to node.js version 4.4.2
* Wed Mar 23 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.4.1-1
- Updated to node.js version 4.4.1
* Thu Mar 10 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.4.0-1
- Updated to node.js version 4.4.0
* Thu Mar  3 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.3.2-1
- Updated to node.js version 4.3.2
* Thu Feb 18 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.3.1-1
- Updated to node.js version 4.3.1
* Wed Feb 10 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.3.0-1
- Updated to node.js version 4.3.0
* Mon Feb  1 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.6-1
- Updated to node.js version 4.2.6
* Thu Jan 21 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.5-1
- Updated to node.js version 4.2.5
* Thu Dec 24 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.4-1
- Updated to node.js version 4.2.4
* Mon Dec 14 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.3-2
- Building with a pre-installed ICU (system-icu) #52
* Fri Dec  4 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.3-1
- Updated to node.js version 4.2.3
* Wed Nov 18 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.2-2
- Cleaning up hardcoded paths and added path macros.
* Fri Nov  6 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.2-1
- Updated to node.js version 4.2.2
* Tue Oct 20 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.1-2
- Fix compilation on el5 (icu)
* Wed Oct 14 2015 Blair Gillam <blair.gillam@breachintelligence.com>
- Updated url to use HTTPS
* Wed Oct 14 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.1-1
- Updated to node.js version 4.2.1
* Tue Oct 13 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.2.0-1
- Updated to node.js version 4.2.0
* Tue Oct  6 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.1.2-1
- Updated to node.js version 4.1.2
* Thu Sep 24 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.1.1-1
- SCL is no longer needed in BuildRequires, move to Makefile.
- Updated to node.js version 4.1.1
* Fri Sep 18 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.1.0-2
- Fixed el6 build env preferences #43
* Thu Sep 17 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.1.0-1
- Updated to node.js version 4.1.0
* Mon Sep 14 2015 Kazuhisa Hara <kazuhisya@gmail.com> - 4.0.0-1
- Updated to node.js version 4.0.0
* Thu Jul  9 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.7
* Mon Jul  6 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.6
- Fix building on RHEL5 by @Gillingham
- Update specfile to use gyp patch by @Gillingham
* Tue Jun 23 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.5
* Mon May 25 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.4
* Thu May 14 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.3
* Wed Apr  1 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.2
* Wed Mar 25 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.1
- Fixed dependency to python27 by @Gillingham and @kvervo
- Fixed BuildRequires by @no1youknowz
* Mon Feb  9 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.12.0
* Tue Feb  3 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.36
* Tue Feb  3 2015 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.35
* Thu Dec 18 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.34
* Fri Oct 24 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.33
* Wed Sep 17 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.32
* Wed Aug 20 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.31
* Fri Aug  1 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.30
* Fri Jul 25 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed #33 some manfile conflict
* Thu Jun 19 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.29
* Wed May  7 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.28
* Wed May  7 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.27
- Removed dtrace file
* Wed Feb 19 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.26
* Mon Jan 27 2014 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.25
* Mon Dec 23 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.24
* Thu Dec 12 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.23
* Thu Nov 14 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.22
* Mon Oct 28 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Moved Obsoletes tag
* Tue Oct 22 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.21 by @blackbeam
* Thu Oct  3 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.20 by @fjordansilva
* Wed Sep 25 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.19
* Fri Sep 13 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Apply the man file of npm package
* Thu Sep 12 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Dividing core and npm #25
* Sun Sep  8 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.18 by @fjordansilva
* Thu Aug 22 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.17
* Sat Aug 17 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.16
* Fri Jul 26 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.15
* Fri Jul 26 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.14
* Wed Jul 10 2013 Fernando Jordan <fjordansilva@gmail.com>
- Updated to node.js version 0.10.13
* Sat Jun 22 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.12
* Tue Jun 18 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.11
* Fri Jun  7 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.10
* Sat Jun  1 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.9
* Sun May 26 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.8
* Tue May 21 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.7
* Thu May 16 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.6
* Wed May  1 2013 Andrew Grimberg <agrimberg@linuxfoundation.org>
- Updated to node.js version 0.10.5
* Fri Apr 19 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.4
* Fri Apr  5 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.3
* Tue Apr  2 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.2
* Wed Mar 27 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.1
* Wed Mar 27 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.10.0
* Thu Mar 14 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.22
* Thu Feb 28 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.21
* Fri Feb 22 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.20 by @laapsaap
- Fixed #14
* Tue Feb 12 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.19
- Make formatting more consistent by @adambrod
- Cleanup of the files section, removes warning by @steevel
* Sun Jan 20 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.18
* Sun Jan 13 2013 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.17
* Sun Dec 30 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Added patch for CentOS and some BuildRequires by @smellman
* Mon Dec 17 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.16
* Sun Dec  2 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.15
- Fix build failure on i386 arch by @symm
* Sun Oct 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.14 by @Pitel
* Thu Oct 18 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed issues #9, Unneeded dependency on git
* Wed Oct 17 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed missing spaces for Fedora 18 (syntax error)
- Added BuildRequires: tar
* Mon Oct 15 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.12 by @brandonramirez
* Sat Sep 29 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.11
- Making Source0 "spectool friendly" by @elus
* Wed Sep 12 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.9
- Added build dependency by @knalli
- Fixed missing spaces (syntax error) by @knalli
* Thu Aug 23 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.8
* Sun Aug 19 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.7
- Added Architecture check
- Build came to pass in "make binary" a single
* Sat Aug 11 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.6
- Added as a package to build a binary tarball
- Various minor fixes and improvements
* Sun Aug  5 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.5
* Sat Jul 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.4
* Sat Jul 28 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Fixed issues #4, workaround for Avoid having to
- remove the rpm in the installation section
* Fri Jul 20 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.3
* Fri Jul  6 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.1
* Tue Jun 26 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.8.0
* Sun Jun 10 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.19
* Fri May 18 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.18
* Mon May  7 2012 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.17
* Sat Apr 14 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.15
* Sat Mar 31 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.14
* Tue Mar 20 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.13
* Sat Mar  3 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.12
* Sun Feb  5 2012 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.10
* Sat Jan  7 2012 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.7
* Fri Dec 16 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.6
* Sun Dec  4 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.6.5
* Tue Nov 29 2011 Pete Fritchman <petef@databits.net>
- Updated to node.js version 0.6.3
* Tue Oct 11 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.9
* Sun Oct  2 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.8
* Sun Sep 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.7
* Sat Sep 10 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.6
* Mon Aug 29 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.5
* Fri Aug 12 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.4
* Wed Aug  3 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.5.3
* Tue Jul 19 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Initial version
