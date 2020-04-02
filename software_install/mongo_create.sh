#!/bin/bash
read -p "Input container name:" container
read -p "Input container port:" port
base_dir="/$container"

config_dir="$base_dir/config"
mkdir -p $config_dir
echo "MongoDB容器配置目录 $config_dir 已创建"

data_dir="$base_dir/data"
mkdir -p $data_dir
echo "MongoDB容器数据目录 $data_dir 已创建"

conf_file="$config_dir/mongod.conf.orig"
touch $conf_file
echo "MongoDB容器配置文件 $conf_file 已创建"

cat >> $conf_file << EOF
# mongod.conf

# for documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where and how to store data.
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true
#  engine:
#  mmapv1:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

# network interfaces
net:
  port: 27017
#  bindIp: 127.0.0.1


# how the process runs
processManagement:
  timeZoneInfo: /usr/share/zoneinfo
EOF

docker run --name $container -p $port:27017 -v $data_dir:/var/lib/mongodb -v $conf_file:/etc/mongod.conf.orig -di mongo:4 --auth

echo "MongoDB容器创建结果为："
docker ps -a | grep $container