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

sudo rm /etc/nginx/sites-enabled/nginx_test.conf

check_status "停止nginx测试失败，需要使用root权限执行此脚本"
