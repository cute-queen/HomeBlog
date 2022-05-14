#! /bin/bash

# 获取到文件夹

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

python3 './scripts/create_file.py'

check_status "创建配置文件失败"