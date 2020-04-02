#!/bin/bash
yum update -y
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum -y install docker-ce
echo "Docker 安装的版本："
docker -v
mkdir -p /etc/docker
touch /etc/docker/daemon.json
cat >> /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://tai7pwst.mirror.aliyuncs.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker

echo "Docker 安装成功"
