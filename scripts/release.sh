#! /bin/bash

# 获取到文件夹

current_path="$PWD"

check_status() {
  if [ $? -ne 0 ]; then
	  echo $1 >&2
	  exit 2
  fi
}

check_create_folder() {
  if [ ! -d $1 ];then
  mkdir $1
  fi
}

check_remove_file() {
  if [ -d $1 ];then
    sudo rm $1
  fi
}

# 工作目录
work_path=$(dirname "$PWD")

cd $work_path

check_create_folder temp

check_create_folder logs

python3 './scripts/create_file.py'

check_status "创建配置文件失败"

# 安装json解析库
sudo apt-get install jq

check_status "安装json解析库失败"


site_name=$(cat ${work_path}/conf/settings.json | jq -r .website)

nginx_file="${work_path}/temp/${site_name}.conf"

check_remove_file nginx_file

sudo ln -s $nginx_file /etc/nginx/sites-enabled

sudo /etc/init.d/nginx restart