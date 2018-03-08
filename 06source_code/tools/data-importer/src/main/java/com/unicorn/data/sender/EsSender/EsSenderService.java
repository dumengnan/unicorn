package com.unicorn.data.sender.EsSender;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.elasticsearch.spark.streaming.api.java.JavaEsSparkStreaming;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.Tuple2;

/**
 * Created by Administrator on 2018/3/8.
 */
public class EsSenderService {

    private Logger logger = LoggerFactory.getLogger(getClass());

    private String esCollection = "unicorn/data";

    public void sendDataToEs(JavaInputDStream<ConsumerRecord<String, String>> stream) {
        JavaPairDStream<String, String> topicToDataPair = stream
                .mapToPair(record -> new Tuple2<>(record.key(), record.value()));

        JavaEsSparkStreaming.saveToEsWithMeta(topicToDataPair, esCollection);
    }
}
