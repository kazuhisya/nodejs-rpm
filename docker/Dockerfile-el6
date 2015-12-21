FROM centos:6
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y centos-release-scl-rh epel-release && \
    yum install -y yum-utils rpmdevtools make git devtoolset-3-gcc-c++ devtoolset-3-binutils python27

COPY / /nodejs-rpm
WORKDIR /nodejs-rpm

RUN yum-builddep -y ./nodejs.spec
RUN scl enable python27 devtoolset-3 'make rpm'
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/nodejs-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-npm-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-devel-[^d.+].*
CMD ["node", "-v"]
