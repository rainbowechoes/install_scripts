#!/bin/bash
read -p "Input need remove container's name:" container

docker stop $container && docker rm $container

echo "容器已停止并删除"
