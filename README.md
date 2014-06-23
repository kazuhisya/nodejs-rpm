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
*  This spec is tested under el6 and el5 only.
However, Fedora15 or later work. maybe.

### RHEL/CentOS/SL/OL 6 or 7

    $ sudo yum install -y rpm-build rpmdevtools openssl-devel zlib-devel redhat-rpm-config gcc gcc-c++ make libstdc++-devel
    $ rpmdev-setuptree

    $ cd /path/to/nodejs-rpm # git dir
    $ ./build.sh
    $ cd ~/rpmbuild/RPMS/x86_64/
    $ sudo yum install ./nodejs-X.X.X-X.el6.x86_64.rpm ./nodejs-npm-X.X.X-X.el6.x86_64.rpm --nogpgcheck

### RHEL/CentOS/SL/OL 5

when you try to build on el5, must enable the EPEL repository.

    $ sudo rpm -ivh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
    $ sudo yum install -y rpm-build rpmdevtools openssl-devel zlib-devel python26 gcc gcc-c++ make libstdc++-devel
    $ mkdir ~/rpmbuild
    $ cd ~/rpmbuild
    $ rpmdev-setuptree

    $ cd /path/to/nodejs-rpm # git dir
    $ ./build.sh
    $ cd ~/rpmbuild/RPMS/x86_64/
    $ sudo yum install ./nodejs-X.X.X-X.x86_64.rpm ./nodejs-npm-X.X.X-X.x86_64.rpm --nogpgcheck
