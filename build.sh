#!/bin/bash
set -e

RPMBUILD_DIR=`rpm --eval %{_topdir}`

pushd `dirname $0` > /dev/null
NODEJSRPM_DIR=$(pwd)
popd > /dev/null

cd $RPMBUILD_DIR/SOURCES
cp $NODEJSRPM_DIR/*.patch .
cd -

cd $RPMBUILD_DIR/SPECS
cp $NODEJSRPM_DIR/*.spec .
cd -

spectool -g -R $RPMBUILD_DIR/SPECS/nodejs.spec
rpmbuild --clean -ba $RPMBUILD_DIR/SPECS/nodejs.spec
