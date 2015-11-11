FROM centos:7
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN yum install -y yum-utils rpmdevtools make git
RUN git clone https://github.com/kazuhisya/nodejs-rpm.git

WORKDIR /nodejs-rpm
RUN yum-builddep -y ./nodejs.spec
RUN make rpm
RUN yum install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/nodejs-*.rpm
CMD ["node", "-v"]
