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


setting up:

```bash
$ sudo yum install -y yum-utils rpmdevtools make
```

git clone and make:

```bash
$ git clone https://github.com/kazuhisya/nodejs-rpm.git
$ cd nodejs-rpm
$ sudo yum-builddep ./nodejs.spec
$ make rpm
```

install package:

```bash
$ cd ./dist/RPMS/x86_64/
$ sudo yum install ./nodejs-X.X.X-X.el6.x86_64.rpm ./nodejs-npm-X.X.X-X.el6.x86_64.rpm --nogpgcheck
```
