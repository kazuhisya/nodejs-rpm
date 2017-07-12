FROM centos:7
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y yum-utils rpmdevtools make
COPY / /nodejs-rpm
WORKDIR /nodejs-rpm

RUN yum-builddep -y ./nodejs.spec
RUN make rpm
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/nodejs-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-npm-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-devel-[^d.+].*
RUN yum install -y epel-release && yum install -y copr-cli
CMD ["node", "-v"]
