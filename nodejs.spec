%define   _base node
%define   _includedir %{_prefix}/include
%define   _bindir %{_prefix}/bin
%define   _libdir %{_prefix}/lib
%define   _node_original_docdir /usr/share/doc/node
%define   _build_number %(echo ${BUILD_NUMBER:-1})

%if 0%{?rhel} == 5
%define   _datarootdir%{_datadir}
%endif

%global tapsetroot %{_prefix}/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{_build_cpu}

Name:          %{_base}js
Version:       9.11.1
Release:       %{_build_number}%{?dist}
Provides:      %{_base}js(engine)
Summary:       Node.js is a server-side JavaScript environment that uses an asynchronous event-driven model.
Packager:      Kazuhisa Hara <kazuhisya@gmail.com>
Group:         Development/Libraries
License:       MIT License
URL:           https://nodejs.org
Source0:       %{url}/dist/v%{version}/%{_base}-v%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-tmp
Prefix:        /usr
BuildRequires: tar
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: libstdc++-devel
BuildRequires: zlib-devel
BuildRequires: gzip
BuildRequires: python

%{?el5:BuildRequires: python27}
%{?el5:BuildRequires: redhat-rpm-config}

Patch0: node-js.centos5.configure.patch
Patch1: node-js.centos5.gyp.patch
Patch2: node-js.centos5.icu.patch
Patch3: node-js.v8_inspector.gyp.patch
Patch4: node-js.node.gyp-python27.patch

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

%if 0%{?rhel} == 5
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%endif

%build
%if 0%{?rhel} == 5
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
mv $RPM_BUILD_ROOT%{_node_original_docdir}/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{_base}-v%{version}/
rm -rf $RPM_BUILD_ROOT%{_node_original_docdir}
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
%{_mandir}/man1/node*

%files binary
%defattr(-,root,root,-)
%{_datarootdir}/%{_base}js/%{_base}-v%{version}-linux-%{_node_arch}.tar.gz

%files npm
%defattr(-,root,root,-)
%{_libdir}/node_modules/npm
%{_bindir}/npm
%{_bindir}/npx

%doc
%{_mandir}/man1/npm*
%{_mandir}/man5
%{_mandir}/man7

%files devel
%{_includedir}/node/
%{tapsetroot}

%changelog
* Thu Apr  5 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.11.1-1
- updated to node.js version 9.11.1
* Thu Apr  5 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.11.0-1
- updated to node.js version 9.11.0
* Fri Mar 30 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.10.1-1
- updated to node.js version 9.10.1
* Thu Mar 29 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.10.0-1
- updated to node.js version 9.10.0
* Thu Mar 29 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.9.0-1
- updated to node.js version 9.9.0
* Thu Mar  8 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.8.0-1
- updated to node.js version 9.8.0
* Wed Mar  7 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.7.1-1
- updated to node.js version 9.7.1
* Fri Feb 23 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.7.0-1
- updated to node.js version 9.7.0
* Fri Feb 23 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.6.1-1
- updated to node.js version 9.6.1
* Thu Feb  1 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.5.0-1
- updated to node.js version 9.5.0
* Thu Jan 11 2018 Kazuhisa Hara <kazuhisya@gmail.com> - 9.4.0-1
- updated to node.js version 9.4.0
* Wed Dec 13 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 9.3.0-1
- updated to node.js version 9.3.0
* Wed Dec 13 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 9.2.1-1
- updated to node.js version 9.2.1
* Wed Nov 15 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 9.2.0-1
- updated to node.js version 9.2.0
* Wed Nov  8 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 9.1.0-1
- updated to node.js version 9.1.0
* Wed Nov  1 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 9.0.0-1
- updated to node.js version 9.0.0
* Wed Nov  1 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.9.0-1
- updated to node.js version 8.9.0
* Thu Oct 26 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.8.1-1
- updated to node.js version 8.8.1
* Wed Oct 25 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.8.0-1
- updated to node.js version 8.8.0
* Thu Oct 12 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.7.0-1
- updated to node.js version 8.7.0
* Fri Oct  6 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.6.0-1
- updated to node.js version 8.6.0
* Wed Sep 13 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.5.0-1
- updated to node.js version 8.5.0
* Wed Aug 16 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.4.0-1
- updated to node.js version 8.4.0
* Thu Aug 10 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.3.0-1
- updated to node.js version 8.3.0
* Fri Jul 21 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.2.1-1
- updated to node.js version 8.2.1
* Thu Jul 20 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.2.0-1
- updated to node.js version 8.2.0
- added npx command
* Wed Jul 12 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.1.4-1
- updated to node.js version 8.1.4
* Fri Jun 30 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.1.3-1
- updated to node.js version 8.1.3
* Fri Jun 16 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.1.2-1
- updated to node.js version 8.1.2
* Wed Jun 14 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.1.1-1
- updated to node.js version 8.1.1
* Tue Jun 13 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.1.0-1
- updated to node.js version 8.1.0
* Wed May 31 2017 Kazuhisa Hara <kazuhisya@gmail.com> - 8.0.0-1
- updated to node.js version 8.0.0
