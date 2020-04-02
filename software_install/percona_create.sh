#!/bin/bash
read -p "Input container name:" container
read -p "Input container port:" port

# Percona容器的基本目录
base_dir="/$container/"

data_dir="$base_dir/data"
mkdir -p $data_dir
echo "Percona容器数据目录 $data_dir 已创建"

log_dir="$base_dir/log"
mkdir -p $log_dir
echo "Percona容器日志目录 $log_dir 已创建"

conf_file="$base_dir/mysqld.cnf"
touch $conf_file
echo "Percona容器配置文件 $conf_file 已创建"

cat >> $conf_file << EOF
[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
# datadir=/var/lib/mysql
datadir=/percona/data
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

#log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
character-set-server=utf8
EOF

chown -R 999 $base_dir

docker run --name=$container -p $port:3306 -e MYSQL_ROOT_PASSWORD=root -v $data_dir:/percona/data -v $log_dir:/percona/log -v $conf_file:/etc/percona-server.conf.d/mysqld.cnf -di percona

echo "Percona容器创建结果为："
docker ps -a | grep $container
