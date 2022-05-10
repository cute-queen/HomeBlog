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

sudo ln -s "$work_path/conf/nginx_test.conf" /etc/nginx/sites-enabled

check_status "启用nginx测试失败，请使用root权限启用此脚本"

sudo /etc/init.d/nginx restart

check_status "重启nginx失败，检查nginx是否安装成功"

echo "启动nginx测试成功，打开浏览器访问nginx是否正常"