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
  if [ -f $1 ];then
    sudo rm $1
  fi
}

check_install_app() {
  local ret='0'
  command -v $1 >/dev/null 2>&1 || { local ret='1'; }

  # fail on non-zero return value
  if [ "$ret" -ne 0 ]; then
    sudo apt-get install $1
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
check_install_app jq

site_name=$(cat ${work_path}/conf/settings.json | jq -r .website)

nginx_file="${work_path}/temp/${site_name}.conf"

check_remove_file "/etc/nginx/sites-enabled/${site_name}.conf"

sudo ln -s $nginx_file /etc/nginx/sites-enabled

sudo /etc/init.d/nginx restart

# uwsgi开启
if [ -f "${work_path}/temp/${site_name}.pid" ];then
  uwsgi --stop "${work_path}/temp/${site_name}.pid"
fi

uwsgi --start "${work_path}/temp/${site_name}.ini"