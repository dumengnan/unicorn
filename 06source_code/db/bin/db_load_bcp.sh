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
. $DIR/../etc/db.config


log_file=$DIR/../logs/db_load_bcp.log


function log() {
   msg=$1
   now=`date +"%Y-%m-%d %H:%M:%S"`
   echo -e "$now    $msg" >> $log_file
}

function load_bcp_to_db() {
   file_list=$1
   for file in $file_list; do
        log "Load File: $file To Db social " 
        log "mysql -uroot -p$PASSWORD $DATABASE -e \"LOAD DATA INFILE \'$file\'  INTO TABLE social_user FIELDS TERMINATED BY \'\t\'  ENCLOSED BY \'\"\' LINES TERMINATED BY \'\n\' IGNORE 0 ROWS\"";
        mysql -uroot -p$PASSWORD $DATABASE -e "LOAD DATA INFILE '$file'  INTO TABLE social_user FIELDS TERMINATED BY '\t'  ENCLOSED BY '\"' LINES TERMINATED BY '\n' IGNORE 0 ROWS";
        if [ $? == 0 ];then
           log "load $file To Db Success!"
        else 
           log "load $file To Db Failed" 
        fi
   done 
}

function main() {

    while true; do
        file_list=`find $DATA_DIR -type f -name "uni-*.bcp"`

        sleep 10

        if [ -z "$file_list" ];then
          log "Not Found Bcp Files"
          continue
        else 
           load_bcp_to_db $file_list
        fi  

    done 
}

main