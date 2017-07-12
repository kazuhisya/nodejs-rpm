#!/bin/bash
set -e
project_name=nodejs
copr_login=$COPR_LOGIN
copr_username=$COPR_USERNAME
copr_token=$COPR_TOKEN
spec_file=${project_name}.spec


mkdir -p ~/.config
cat > ~/.config/copr <<EOF
[copr-cli]
login = ${copr_login}
username = ${copr_username}
token = ${copr_token}
copr_url = https://copr.fedoraproject.org
EOF

version=`awk '$1=="Version:" {print $2}' ${spec_file}`
release=`awk '/BUILD_NUMBER/ {print $4}' nodejs.spec | tr -d '${BUILD_NUMBER:-' | tr -d '})'`
srpm_file=./dist/SRPMS/${project_name}-${version}-${release}.el7.centos.src.rpm
copr-cli build --nowait ${project_name} ${srpm_file}


