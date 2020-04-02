#!/bin/bash
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install -y libffi-devel zlib1g-dev
yum install zlib* -y
tar -xvJf Python-3.6.8.tar.xz
mkdir /usr/local/python3
cd Python-3.6.8
./configure --prefix=/usr/local/python3 --enable-optimizations --with-ssl
make && make install
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
python3 -V
pip3 -V
cd ~
mkdir .pip
cd .pip
rm -rf pip.conf
touch pip.conf
cat >>pip.conf <<EOF
[global]
timeout = 6000
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
pip3 install --upgrade pip
echo "python3 安装成功"
