FROM opensuse:42.1
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN zypper addrepo http://download.opensuse.org/repositories/devel:/tools/openSUSE_Leap_42.1/devel:tools.repo
RUN zypper --gpg-auto-import-keys install --no-confirm --auto-agree-with-licenses \
        curl \
        gcc \
        gcc-c++ \
        gzip \
        libstdc++-devel \
        make \
        openssl-devel \
        rpm-build \
        spectool \
        tar \
        wget \
        yum-utils \
        zlib-devel
COPY / /nodejs-rpm
WORKDIR /nodejs-rpm

RUN make rpm
RUN zypper --no-gpg-checks install --no-confirm \
        ./dist/RPMS/x86_64/nodejs-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-npm-[^d.+].* \
        ./dist/RPMS/x86_64/nodejs-devel-[^d.+].*
CMD ["node", "-v"]
