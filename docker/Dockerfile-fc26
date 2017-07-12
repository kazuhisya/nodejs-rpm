FROM fedora:26
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN dnf install -y dnf-plugins-core rpmdevtools make
COPY / /nodejs-rpm
WORKDIR /nodejs-rpm

RUN dnf builddep -y ./nodejs.spec
RUN make rpm
RUN dnf install -y \
        --nogpgcheck \
        ./dist/RPMS/x86_64/nodejs-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-npm-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-devel-[^d.+].*
CMD ["node", "-v"]
