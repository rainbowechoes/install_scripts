#!/bin/bash
yum install -y wget
yum install -y gcc-c++
yum install -y zlib-devel perl-ExtUtils-MakeMaker
# 处理高版本安装问题，详见https://stackoverflow.com/questions/17915098/openssl-ssl-h-no-such-file-or-directory-during-installation-of-git
yum install -y curl-devel expat-devel gettext-devel openssl-devel zlib-devel
yum -y install unzip
unzip git-2.25.1.zip
cd git-2.25.1
make prefix=/usr/local all
make prefix=/usr/local install
echo "离线安装结果:"
git --version
