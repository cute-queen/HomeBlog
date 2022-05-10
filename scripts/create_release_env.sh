#!/bin/sh

# 定义一个函数，执行命令a，如果执行失败，则执行命令b

current_path="$PWD"

check_status() {
  if [ $? -ne 0 ]; then
	  echo $1 >&2
	  exit 2
  fi
}

# 工作目录
work_path=$(dirname "$PWD")

cd $work_path

# 创建python虚拟环境
python3 -m venv venv

check_status "创建虚拟环境失败，请检查python环境是否安装"

# 
