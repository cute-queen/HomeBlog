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

mkdir temp
mkdir logs

python3 './scripts/create_file.py'

check_status "创建配置文件失败"

# 安装json解析库
sudo apt-get install jq

check_status "安装json解析库失败"

site_name = $(cat ${work_path}/conf/settings.json | jq .website)

echo $site_name

nginx_file = '${work_path}/temp/${site_name}.conf'

echo $nginx_file