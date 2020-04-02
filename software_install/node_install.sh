#!/bin/bash
# 输入版本，比如：12.16.1
read -p "输入要安装的版本：" version
yum install -y wget
url="https://npm.taobao.org/mirrors/node/v${version}/node-v${version}-linux-x64.tar.xz"
wget $url
nodefile="node-v${version}-linux-x64.tar.xz"
tar -xvf $nodefile
mv node-v${version}-linux-x64 /usr/local/nodejs
# read -p "输入node安装包的位置：" location
# ln -s ${location}/nodejs/bin/node /usr/local/bin/
# ln -s ${location}/nodejs/bin/npm /usr/local/bin/
cat >>/etc/profile <<EOF
export PATH=/usr/local/nodejs/bin:$PATH
EOF
source /etc/profile
npm config set registry https://registry.npm.taobao.org/
echo "node 安装结果"
node -v
npm -v
npm config get registry
