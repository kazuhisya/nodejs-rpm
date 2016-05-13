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
Version:       4.4.3
Release:       1%{?dist}.gd
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
* Thu Apr 14 2016 Kazuhisa Hara <kazuhisya@gmail.com> - 4.4.3-1
- Updated to node.js version 4.4.3
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
