package com.unicorn.data.sender.HbaseSender;


import com.google.common.collect.Lists;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonPrimitive;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.twitter.bijection.Injection;
import com.twitter.bijection.avro.GenericAvroCodecs;
import com.unicorn.data.sender.HbaseSender.bean.EntityValue;
import com.unicorn.data.utils.UnicornConstant;
import com.unicorn.data.utils.UnicornDataImportUtil;
import java.io.IOException;
import java.io.Serializable;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.apache.avro.Schema;
import org.apache.avro.generic.GenericRecord;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.configuration.Configuration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.api.java.function.PairFlatMapFunction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.Tuple2;

/**
 * Created by Administrator on 2018/5/9.
 */
public class HbaseSenderService implements Serializable {
    private static Logger log = LoggerFactory.getLogger(HbaseSenderService.class);

    private Map<String, Schema> schemaMap;
    private List<String> extractWordList;

    private Segment segment;

    public HbaseSenderService(Configuration configuration) throws IOException {
        List<String> extractWordList = configuration.getList("extract.word.list");
        String avroSchemaDir = configuration.getString("avro.schema.dir");
        String[] topicList = configuration.getStringArray("topics");

        this.schemaMap = UnicornDataImportUtil.loadAvroSchemaFromFile(avroSchemaDir, topicList);
        this.extractWordList = extractWordList;
        this.segment =  HanLP.newSegment().enableNameRecognize(true).enableOrganizationRecognize(true).enablePlaceRecognize(true);
    }


    public class ConvertToPut implements PairFlatMapFunction<ConsumerRecord<String, byte[]>, ImmutableBytesWritable, Put> {

        @Override
        public Iterator<Tuple2<ImmutableBytesWritable, Put>> call(ConsumerRecord<String, byte[]> avroConsumerRecord)
                throws Exception {
            List<Tuple2<ImmutableBytesWritable, Put>> result = Lists.newArrayList();

            String topic = avroConsumerRecord.topic();
            if (!schemaMap.containsKey(topic)) {
                log.error("Can not Find Topic {} Schema !", topic);
                return result.iterator();
            }

            Gson gson = new GsonBuilder().serializeNulls().create();

            Injection<GenericRecord, byte[]> recordInjection = GenericAvroCodecs.toBinary(schemaMap.get(topic));
            GenericRecord record = recordInjection.invert(avroConsumerRecord.value()).get();

            String content = (String) record.get("content");
            String rowKey = createRowKey(record);
            String qualifier = DigestUtils.md5Hex(content);

            List<String> keyWordList = HanLP.extractKeyword(content, UnicornConstant.keyWordSize);
            Put keyWordPut = new Put(Bytes.toBytes(rowKey));
            keyWordPut.add(Bytes.toBytes(UnicornConstant.KEY_WORD_FAMILY), Bytes.toBytes(qualifier), Bytes.toBytes(gson.toJson(keyWordList)));
            Tuple2<ImmutableBytesWritable, Put> keyWordTuple = new Tuple2<>(new ImmutableBytesWritable(), keyWordPut);
            result.add(keyWordTuple);

            List<EntityValue> entityValue = parseEntityValue(content);
            Put entityPut = new Put(Bytes.toBytes(rowKey));
            entityPut.add(Bytes.toBytes(UnicornConstant.ENTITY_FAMILY), Bytes.toBytes(qualifier), Bytes.toBytes(gson.toJson(entityValue)));
            Tuple2<ImmutableBytesWritable, Put> entityTuple = new Tuple2<>(new ImmutableBytesWritable(), entityPut);
            result.add(entityTuple);

            return result.iterator();
        }

        public List<EntityValue> parseEntityValue(String content) {
            List<EntityValue> entityValues = Lists.newArrayList();
            for (Term term : segment.seg(content)) {
                // 只抽取指定类型的词（人名 机构名 后期需要添加码址识别）
                if (extractWordList.contains(term.nature.name())) {
                    EntityValue entityValue = new EntityValue(term.nature.name(), term.word);
                    entityValues.add(entityValue);
                }
            }
            return entityValues;
        }

        public String createRowKey(GenericRecord record) {
            String socialType = (String) record.get("social_type");
            String statusId = (String) record.get("status_id");

            JsonArray jsonArray = new JsonArray();
            jsonArray.add(new JsonPrimitive(socialType));
            jsonArray.add(new JsonPrimitive(statusId));

            return jsonArray.toString();
        }
    }

}
