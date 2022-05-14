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

while getopts u:p: opt;
do
case $opt in
u) user = $OPTARG
   ;;
p) port = $OPTARG
   ;;
?) echo "$opt is an invalid option"
   ;;
esac
done

echo '$user $port'