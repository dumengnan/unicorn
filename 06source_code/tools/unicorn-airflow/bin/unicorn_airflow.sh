#！/bin/bash

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

# 获取到真实路径, 防止在软连接里面
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

cd $DIR


export AIRFLOW_HOME="$(dirname "$DIR")"
export PATH=$AIRFLOW_HOME/bin:$PATH
export AIRFLOW_SERVER_IP=`hostname -I | cut -f1 -d ' '`

if [ -f unicorn_airflow.env ];then 
    source unicorn_airflow.env 
fi

exec python $DIR/unicorn_airflow.py $@