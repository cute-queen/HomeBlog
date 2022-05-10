#! /bin/bash

# 此脚本用于安装博客部署所需的程序

# 检查命令执行是否成功
check_status() {
  if [ $? -ne 0 ]; then
	  echo $1 >&2
	  exit 2
  fi
}

# 工作目录
work_path=$(dirname "$PWD")

echo "$work_path/conf/nginx_test.conf"