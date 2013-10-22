#!/bin/bash
set -e

RPMBUILD_DIR=${RPMBUILD_DIR:-$HOME/buildrpm}
NODEJS_VERSION=${NODEJS_VERSION:-v0.10.20}
NODEJS_SRC=${NODEJS_SRC:-http://nodejs.org/dist/$NODEJS_VERSION/node-$NODEJS_VERSION.tar.gz}

pushd `dirname $0` > /dev/null
NODEJSRPM_DIR=$(pwd)
popd > /dev/null

cd $RPMBUILD_DIR/SOURCES
wget $NODEJS_SRC
cp $NODEJSRPM_DIR/*.patch .
cd -

cd $RPMBUILD_DIR/SPECS
cp $NODEJSRPM_DIR/*.spec .
cd -

spectool -g -R $RPMBUILD_DIR/SPECS/nodejs.spec
rpmbuild --clean -ba $RPMBUILD_DIR/SPECS/nodejs.spec
