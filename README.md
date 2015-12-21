#  node.js RPM spec

Master: [![Circle CI](https://circleci.com/gh/kazuhisya/nodejs-rpm/tree/master.svg?style=shield)](https://circleci.com/gh/kazuhisya/nodejs-rpm/tree/master)

LTS: [![Circle CI](https://circleci.com/gh/kazuhisya/nodejs-rpm/tree/LTS.svg?style=shield)](https://circleci.com/gh/kazuhisya/nodejs-rpm/tree/LTS)


- node.js rpm spec : https://github.com/kazuhisya/nodejs-rpm
- node.js source   : https://nodejs.org/dist/

# Compiled Package

- You can find prebuilt rpm binary from here(el7 and fc23)
    - Stable Release: [FedoraCopr khara/nodejs Copr](https://copr.fedoraproject.org/coprs/khara/nodejs/)
    - LTS Release: [FedoraCopr khara/nodejs-lts Copr](https://copr.fedoraproject.org/coprs/khara/nodejs-lts/)

el7:

```bash
$ sudo curl -sL -o /etc/yum.repos.d/khara-nodejs.repo https://copr.fedoraproject.org/coprs/khara/nodejs/repo/epel-7/khara-nodejs-epel-7.repo
$ sudo yum install -y nodejs nodejs-npm
```

fc23:

```bash
$ sudo dnf copr enable khara/nodejs
$ sudo dnf install -y nodejs nodejs-npm
```

# Building the RPM

## Distro support

### Tested

- RHEL/CentOS 7 x86_64
- Fedora23 x86_64

### Probably it works

- RHEL/CentOS/SL/OL 6 x86_64
    - when you try to build on el6, can use `devtoolset-3` and `SCL` repository
        - RHEL6.x: [Red Hat Developer Toolset 3](https://access.redhat.com/documentation/en-US/Red_Hat_Developer_Toolset/3/) and [Red Hat Software Collections](https://access.redhat.com/documentation/en-US/Red_Hat_Software_Collections/index.html)
        - CentOS6.x: install `centos-release-scl-rh` package.
    - `devtoolset-3-gcc-c++`, `devtoolset-3-binutils`, `python27`

- RHEL/CentOS/SL/OL 5 x86_64
    - when you try to build on el5, you can use `devtoolset-2` and `python27`
        - Developer Toolset 2
            - RHEL5.x: [Red Hat Developer Toolset 2](https://access.redhat.com/documentation/en-US/Red_Hat_Developer_Toolset/2/)
            - CentOS5.x: [devtools-2](http://people.centos.org/tru/devtools-2/readme)
        - Python 2.7
            - [IUS Community Project](https://ius.io/)
	- `devtoolset-2-gcc-c++`, `devtoolset-2-binutils`, `python27`



### Prerequisites:

- Python 2.7
- `gcc` and `g++` 4.8 or newer

## Docker (el7, el6, el5)

Docker environment for building nodejs rpm.
It will help to build and debug.

- See also: [docker/README.md](https://github.com/kazuhisya/nodejs-rpm/blob/master/docker/README.md)
- You can also try this:  [Docker Hub kazuhisya/nodejs-rpm](https://hub.docker.com/r/kazuhisya/nodejs-rpm/) (el7 only)

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
$ sudo yum install -y epel-release ius-release
$ sudo yum install -y yum-utils rpmdevtools redhat-rpm-config tar make openssl-devel libstdc++-devel zlib-devel gzip 
$ sudo yum install -y devtoolset-2-gcc-c++ devtoolset-2-binutils python27
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ rpmdev-setuptree
$ curl -OLk https://nodejs.org/dist/vX.X.X/node-vX.X.X.tar.gz
$ cp *.patch ~/rpmbuild/SOURCES/ ; cp *.md ~/rpmbuild/SOURCES/ ; cp *.tar.gz ~/rpmbuild/SOURCES/ 
$ scl enable devtoolset-2 'rpmbuild -ba ./nodejs.spec'
```
