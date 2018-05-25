package com.unicorn.data.sender.HbaseSender;


import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.twitter.bijection.Injection;
import com.twitter.bijection.avro.GenericAvroCodecs;
import com.unicorn.data.utils.UnicornConstant;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.hadoop.hbase.client.Put;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by Administrator on 2018/5/9.
 */
public class HbaseSenderService {
    private static Logger log = LoggerFactory.getLogger(HbaseSenderService.class);

    private Map<String, Schema> schemaMap;
    private List<String> extractWordList;

    private Segment segment;

    public HbaseSenderService(Map<String, Schema> schemaMap, List<String> extractWordList) {
        this.schemaMap = schemaMap;
        this.extractWordList = extractWordList;
        this.segment =  HanLP.newSegment().enableNameRecognize(true).enableOrganizationRecognize(true).enablePlaceRecognize(true);
    }


    public void sendDataToHbase(Iterator<ConsumerRecord<String, byte[]>> recordIterator) {

        while(recordIterator.hasNext()) {
            ConsumerRecord<String, byte[]> avroRecord = recordIterator.next();
            String topic = avroRecord.topic();
            if (!schemaMap.containsKey(topic)) {
                log.error("Can not Find Topic {} Schema !", topic);
                continue;
            }

            Injection<GenericRecord, byte[]> recordInjection = GenericAvroCodecs.toBinary(schemaMap.get(topic));
            GenericRecord record = recordInjection.invert(avroRecord.value()).get();

            String content = (String) record.get("content");
            List<String> keyWordList = HanLP.extractKeyword(content, UnicornConstant.keyWordSize);

            for (Term term : segment.seg(content)) {
                // 只抽取指定类型的词（人名 机构名 后期需要添加码址识别）
                if (extractWordList.contains(term.nature.name())) {

                }
            }
        }
    }


}
