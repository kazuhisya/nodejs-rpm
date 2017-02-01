FROM centos:5
MAINTAINER Kazuhisa Hara <kazuhisya@gmail.com>

RUN echo "multilib_policy=best" >> /etc/yum.conf && \
    yum install -y curl
RUN curl -OL https://dl.fedoraproject.org/pub/epel/epel-release-latest-5.noarch.rpm && \
    curl -OL https://centos5.iuscommunity.org/ius-release.rpm && \
    curl -Lo /etc/yum.repos.d/devtools-2.repo http://people.centos.org/tru/devtools-2/devtools-2.repo
RUN yum install -y --nogpgcheck ./epel-release-latest-5.noarch.rpm ./ius-release.rpm && \
    yum install -y yum-utils rpmdevtools buildsys-macros make git openssl-devel zlib-devel devtoolset-2-gcc-c++ devtoolset-2-binutils python27

COPY / /nodejs-rpm
WORKDIR /nodejs-rpm

RUN rpmdev-setuptree && \
    curl -OLk https://nodejs.org/dist/v$(grep Version: nodejs.spec | tr -s " "| cut -d " " -f 2)/node-v$(grep Version: nodejs.spec | tr -s " "| cut -d " " -f 2).tar.gz && \
    cp *.patch ~/rpmbuild/SOURCES/ ; cp *.md ~/rpmbuild/SOURCES/ ; cp *.tar.gz ~/rpmbuild/SOURCES/
RUN scl enable devtoolset-2 'PYTHONHTTPSVERIFY=0 rpmbuild -ba ./nodejs.spec'
RUN yum install -y \
        --nogpgcheck \
        ~/rpmbuild/RPMS/x86_64/nodejs-[^d.+].* \
        ~/rpmbuild/RPMS/x86_64/nodejs-npm-[^d.+].* \
        ~/rpmbuild/RPMS/x86_64/nodejs-devel-[^d.+].*
CMD ["node", "-v"]
