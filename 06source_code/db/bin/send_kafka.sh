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

. $DIR/../etc/send_kafka.config
mkdir -p $SUCCESS_BAK_DIR
mkdir -p $FAILED_BAK_DIR

log_file=$DIR/../logs/send_kafka.log


function log() {
   msg=$1
   now=`date +"%Y-%m-%d %H:%M:%S"`
   echo -e "$now    $msg" >> $log_file
}

# 将扫描发送过的文件移走
## param:1 是否发送成功
## param:2 文件路径
function bak_file() {
   is_success=$1
   filePath=$2
   
   if [ "$is_success" != "0" ];then
      log "Send To Kafka Failed !"
      mv $file $FAILED_BAK_DIR
   else 
      log "Send To Kafka Success"  
      mv $file $SUCCESS_BAK_DIR
   fi
}

# 发送kafka
function send_to_kafka() {
   file_list=$1
   for file in $file_list; do
           echo "Send File: $file To Kafka"
           log "Send File: $file To Kafka" 
           filename=`basename "$file" ".bcp"`
           topic_name=`echo $filename | cut -d "-" -f2`
           kafka-console-producer.sh --broker-list localhost:9092 --topic $topic_name < $file
           bak_file $? $file
   done 
}

## 扫描所有的bcp 文件发送kafka
function main() {
    while true; do
        file_list=`find $DATA_DIR -type f -name "*.bcp"`

        sleep 10

        if [ -z "$file_list" ];then
          log "Not Found Bcp Files"
          continue
        else 
           send_to_kafka $file_list
        fi  

    done 
}

main