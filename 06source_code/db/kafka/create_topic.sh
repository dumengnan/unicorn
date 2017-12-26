#! /bin/bash

ZK=localhost:2181

cat topic.list | while read line 
do 
  kafka-topics.sh --zookeeper $ZK --create --topic $line --replication-factor 1 --partitions 1
done
