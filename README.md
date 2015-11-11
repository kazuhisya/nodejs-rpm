#  node.js RPM spec

[![Circle CI](https://circleci.com/gh/kazuhisya/nodejs-rpm.svg?style=shield)](https://circleci.com/gh/kazuhisya/nodejs-rpm)

- node.js rpm spec : https://github.com/kazuhisya/nodejs-rpm
- node.js source   : https://nodejs.org/dist/


# Building the RPM

## Distro support

Tested working (as sane as I could test for) on:

- RHEL/CentOS 7 x86_64
- RHEL/CentOS/SL/OL 6 x86_64
    - when you try to build on el6, can use `devtoolset-3` and `SCL` repository.
        - RHEL6.x: [Red Hat Developer Toolset 3](https://access.redhat.com/documentation/en-US/Red_Hat_Developer_Toolset/3/) , [Red Hat Software Collections](https://access.redhat.com/documentation/en-US/Red_Hat_Software_Collections/index.html)
        - CentOS6.x: [Devtoolset-3](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-3/) , SCL: run `yum install -y centos-release-SCL`
        - `yum install -y devtoolset-3-gcc-c++ python27`
- RHEL/CentOS/SL/OL 5 x86_64
    - when you try to build on el5, you can use `devtoolset-2` (`devtoolset-2-gcc-c++`, `devtoolset-2-binutils`)
        - RHEL5.x: [Red Hat Developer Toolset 2](https://access.redhat.com/documentation/en-US/Red_Hat_Developer_Toolset/2/)
        - CentOS5.x: [devtools-2](http://people.centos.org/tru/devtools-2/readme)
- Fedora 19 x86_64
    - Fedora15 or later work. maybe.



Prerequisites:

- Python 2.7
- `gcc` and `g++` 4.8 or newer


## Build (el7, el6)

setting up:

```bash
$ sudo yum install -y yum-utils rpmdevtools make
```

git clone and make:

```bash
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
# If you want to use the LTS version: git clone -b LTS https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ sudo yum-builddep ./nodejs.spec
```

el7:

```bash
$ make rpm
```

el6 : with Software Collections and Devtoolset

```bash
$ scl enable python27 devtoolset-3 'make rpm'
```

install package:

```bash
$ cd ./dist/RPMS/x86_64/
$ sudo yum install ./nodejs-X.X.X-X.el6.x86_64.rpm ./nodejs-npm-X.X.X-X.el6.x86_64.rpm --nogpgcheck
```

## Build (el5)

el5 : with Devtoolset and python27

```bash
$ sudo yum install -y yum-utils rpmdevtools redhat-rpm-config tar make openssl-devel libstdc++-devel zlib-devel gzip 
$ sudo yum install -y devtoolset-2-gcc-c++ python27
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ rpmdev-setuptree
$ curl -OL https://nodejs.org/dist/vX.X.X/node-vX.X.X.tar.gz
$ cp *.patch ~/rpmbuild/SOURCES/ ; cp *.md ~/rpmbuild/SOURCES/ ; cp *.tar.gz ~/rpmbuild/SOURCES/ 
$ scl enable devtoolset-2 'rpmbuild -ba ./nodejs.spec'
```
