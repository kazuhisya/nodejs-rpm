%define   _base node

Name:          %{_base}js
Version:       0.8.14
Release:       1%{?dist}
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
Packager:      Kazuhisa Hara <kazuhisya@gmail.com>
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org
Source0:       %{url}/dist/v%{version}/%{_base}-v%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Obsoletes:     npm
Provides:      npm
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%package binary
Summary: Node.js build binary tarballs
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org

%description binary
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
rm -rf $RPM_SOURCE_DIR/%{_base}-v%{version}
%setup -q -n %{_base}-v%{version}

%build
%ifarch x86_64
  %define _node_arch x64
%endif
%ifarch i366 i686
  %define _node_arch x86
%endif
if [ -z %{_node_arch} ];then
  echo "bad arch"
  exit 1
fi

./configure \
    --prefix=/usr \
    --shared-openssl \
    --shared-openssl-includes=%{_includedir} \
    --shared-zlib \
    --shared-zlib-includes=%{_includedir}
make binary %{?_smp_mflags}
cd $RPM_SOURCE_DIR
mv $RPM_BUILD_DIR/%{_base}-v%{version}/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz .
rm  -rf %{_base}-v%{version}
tar zxvf %{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%install
rm -rf $RPM_BUILD_ROOT
mkdir  -p $RPM_BUILD_ROOT/usr
cp -Rp $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}/* $RPM_BUILD_ROOT/usr/
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{_base}-v%{version}/

for file in ChangeLog LICENSE README.md ; do
    mv $RPM_BUILD_ROOT/usr/$file $RPM_BUILD_ROOT/usr/share/doc/%{_base}-v%{version}/
done
mkdir -p $RPM_BUILD_ROOT/usr/share/%{_base}js
mv $RPM_SOURCE_DIR/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz $RPM_BUILD_ROOT/usr/share/%{_base}js/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_includedir}/node
%{_includedir}/node/*.h
%{_includedir}/node/uv-private/*.h
%attr(755,root,root) %{_bindir}/node
%attr(755,root,root) %{_bindir}/node-waf
%attr(755,root,root) %{_bindir}/npm
%dir %{_prefix}/lib/node
%dir %{_prefix}/lib/node/wafadmin
%dir %{_prefix}/lib/node/wafadmin/Tools
%{_prefix}/lib/node/wafadmin/*
%{_prefix}/lib/node_modules/npm
%{_prefix}/share/doc/%{_base}-v%{version}/*
%dir %{_prefix}/lib/dtrace/node.d

%doc
/usr/share/man/man1/node.1.gz

%files binary
%defattr(-,root,root,-)
%dir %{_prefix}/share/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz


%changelog
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
  remove the rpm in the installation section
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
* Sat Sep 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
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
