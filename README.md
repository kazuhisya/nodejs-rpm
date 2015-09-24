#  node.js RPM spec
* node.js rpm spec : https://github.com/kazuhisya/nodejs-rpm
* node.js source   : http://nodejs.org/dist/


# Building the RPM

## Distro support

Tested working (as sane as I could test for) on:

* RHEL/CentOS 7 x86_64
* RHEL/CentOS/SL/OL 6 x86_64
* RHEL/CentOS/SL/OL 5 x86_64
* Fedora 19 x86_64
    * This spec is tested under el7, el6 and el5 only.
    * However, Fedora15 or later work. maybe.
    * when you try to build on el5, must enable the EPEL repository.
    * when you try to build on el6, can use `devtoolset-3` and `SCL` repository.
        - RHEL6.x: [Red Hat Developer Toolset](https://access.redhat.com/documentation/en-US/Red_Hat_Developer_Toolset/) , [Red Hat Software Collections](https://access.redhat.com/documentation/en-US/Red_Hat_Software_Collections/index.html)
        - CentOS6.x: [Devtoolset-3](https://www.softwarecollections.org/en/scls/rhscl/devtoolset-3/) , SCL: run `yum install -y centos-release-SCL`
        - `yum install -y devtoolset-3-gcc-c++ python27`

setting up:

```bash
$ sudo yum install -y yum-utils rpmdevtools make
```

git clone and make:

```bash
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ sudo yum-builddep ./nodejs.spec
```

el7:

```bash
$ make rpm
```

el6 :Software Collections and Devtoolset

```bash
$ scl enable python27 devtoolset-3 'make rpm'
```

install package:

```bash
$ cd ./dist/RPMS/x86_64/
$ sudo yum install ./nodejs-X.X.X-X.el6.x86_64.rpm ./nodejs-npm-X.X.X-X.el6.x86_64.rpm --nogpgcheck
```
