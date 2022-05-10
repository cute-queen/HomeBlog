#! /bin/bash

# 此脚本用于安装博客部署所需的程序

# 检查命令执行是否成功
check_status() {
  if [ $? -ne 0 ]; then
	  echo $1 >&2
	  exit 2
  fi
}

cmd_success() {
    return $? -ne 0
}

# 检查nginx是否存在
nginx -v

# 安装nginx
if [ $? -ne 0 ]; then
    echo [password] | sudo -s apt install nginx
    echo "y" >&0
    nginx -v
    check_status "安装nginx失败，请手动安装"
fi