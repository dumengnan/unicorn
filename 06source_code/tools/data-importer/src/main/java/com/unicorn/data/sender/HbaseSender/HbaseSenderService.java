package com.unicorn.data.sender.HbaseSender;


import com.hankcs.hanlp.tokenizer.NLPTokenizer;
import com.twitter.bijection.Injection;
import com.twitter.bijection.avro.GenericAvroCodecs;
import com.unicorn.data.service.UnicornDataImporter;
import java.io.File;
import java.util.Iterator;
import org.apache.avro.Schema;
import org.apache.avro.Schema.Parser;
import org.apache.avro.generic.GenericRecord;
import org.apache.commons.configuration.Configuration;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by Administrator on 2018/5/9.
 */
public class HbaseSenderService {
    private static Logger log = LoggerFactory.getLogger(HbaseSenderService.class);

    private Schema schema;

    public HbaseSenderService(Schema schema) {
        this.schema = schema;
    }


    public void sendDataToHbase(Iterator<ConsumerRecord<String, byte[]>> recordIterator) {


        while(recordIterator.hasNext()) {
            ConsumerRecord<String, byte[]> avroRecord = recordIterator.next();
            Injection<GenericRecord, byte[]> recordInjection = GenericAvroCodecs.toBinary(schema);
            GenericRecord record = recordInjection.invert(avroRecord.value()).get();

            String content = (String) record.get("content");
        }
    }

}
