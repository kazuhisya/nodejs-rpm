%define   _base node

Name:          %{_base}js
Version:       0.4.12
Release:       1%{?dist}
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
Packager:      Kazuhisa Hara <kazuhisya@gmail.com>
Group:         Development/Libraries
License:       MIT License
URL:           http://nodejs.org
Source0:       %{_base}-v%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel

%description
Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
This allows Node.js to get excellent performance based on the architectures of many Internet applications.

%prep
%setup -q -n %{_base}-v%{version}


%build
./configure --prefix=/usr
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_includedir}/node
%{_includedir}/node/*.h
%{_prefix}/lib/pkgconfig/nodejs.pc
%attr(755,root,root) %{_bindir}/node-waf
%dir %{_prefix}/lib/node
%dir %{_prefix}/lib/node/wafadmin
%dir %{_prefix}/lib/node/wafadmin/Tools
%{_prefix}/lib/node/wafadmin/*
%attr(755,root,root) %{_bindir}/node

%doc
/usr/share/man/man1/node.1.gz

%changelog
* Sun Sep 17 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.4.12
* Thu Aug 18 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Updated to node.js version 0.4.11
* Tue Jul 19 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Initial version
