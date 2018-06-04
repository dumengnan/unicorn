#!/bin/sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  current_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$current_dir/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

# 获取当前工作目录
current_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
MYAPPLICATION_HOME="$current_dir"/..

set -x 

spark-submit \
  --class com.unicorn.data.service.UnicornDataImporter \
  --master local[*] \
  $MYAPPLICATION_HOME/lib/*.jar \
  --conf spark.executor.extraClassPath=$MYAPPLICATION_HOME \
  --files $MYAPPLICATION_HOME/etc/config.properties,$MYAPPLICATION_HOME/etc/consumer.properties
  
exit $?
