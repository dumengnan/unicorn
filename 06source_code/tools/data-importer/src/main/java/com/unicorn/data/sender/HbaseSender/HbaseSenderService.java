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
import java.util.Collections;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import jersey.repackaged.com.google.common.collect.Sets;
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

    private transient Map<String, Schema> schemaMap;
    private List<String> extractWordList;

    private transient Segment segment;

    public HbaseSenderService() {}

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

            String topic = avroConsumerRecord.topic();
            if (!schemaMap.containsKey(topic)) {
                log.error("Can not Find Topic {} Schema !", topic);
                return Collections.emptyIterator();
            }


            Injection<GenericRecord, byte[]> recordInjection = GenericAvroCodecs.toBinary(schemaMap.get(topic));
            GenericRecord record = recordInjection.invert(avroConsumerRecord.value()).get();

            return convertRecordToTuple(record).iterator();
        }

        /**
         * 将avro 的一条record  转换成Hbase 里面的Put 格式.
         * @param record avro record data
         * @return Hbase Put List
         */
        public List<Tuple2<ImmutableBytesWritable, Put>> convertRecordToTuple(GenericRecord record) {
            List<Tuple2<ImmutableBytesWritable, Put>> result = Lists.newArrayList();

            Gson gson = new GsonBuilder().serializeNulls().create();

            String content = (String) record.get("text");
            String rowKey = createRowKey(record);
            String qualifier = DigestUtils.md5Hex(content);

            List<String> keyWordList = HanLP.extractKeyword(content, UnicornConstant.keyWordSize);
            Put keyWordPut = new Put(Bytes.toBytes(rowKey));
            keyWordPut.add(Bytes.toBytes(UnicornConstant.KEY_WORD_FAMILY), Bytes.toBytes(qualifier), Bytes.toBytes(gson.toJson(keyWordList)));
            Tuple2<ImmutableBytesWritable, Put> keyWordTuple = new Tuple2<>(new ImmutableBytesWritable(), keyWordPut);
            result.add(keyWordTuple);

            Set<EntityValue> entityValue = parseEntityValue(content);
            Put entityPut = new Put(Bytes.toBytes(rowKey));
            entityPut.add(Bytes.toBytes(UnicornConstant.ENTITY_FAMILY), Bytes.toBytes(qualifier), Bytes.toBytes(gson.toJson(entityValue)));
            Tuple2<ImmutableBytesWritable, Put> entityTuple = new Tuple2<>(new ImmutableBytesWritable(), entityPut);
            result.add(entityTuple);

            return result;
        }

        /**
         * 从内容中抽取所有的实体.
         * @param content content text
         * @return entity value collection
         */
        public Set<EntityValue> parseEntityValue(String content) {
            Set<EntityValue> entityValues = Sets.newHashSet();
            for (Term term : segment.seg(content)) {
                // 只抽取指定类型的词（人名 机构名 后期需要添加码址识别）
                if (extractWordList.contains(term.nature.name())) {
                    EntityValue entityValue = new EntityValue(term.nature.name(), term.word);
                    entityValues.add(entityValue);
                }
            }
            return entityValues;
        }

        /**
         * 根据social_type  和 id  构建hbase rowkey.
         * @param record avro record message.
         * @return hbase rowkey ["sinaweibo","9038434"]
         */
        public String createRowKey(GenericRecord record) {
            String socialType = (String) record.get("social_type");
            String statusId = (String) record.get("status_id");

            JsonArray jsonArray = new JsonArray();
            jsonArray.add(new JsonPrimitive(socialType));
            jsonArray.add(new JsonPrimitive(statusId));

            return jsonArray.toString();
        }
    }


    public void setSchemaMap(Map<String, Schema> schemaMap) {
        this.schemaMap = schemaMap;
    }

    public void setExtractWordList(List<String> extractWordList) {
        this.extractWordList = extractWordList;
    }

    public void setSegment(Segment segment) {
        this.segment = segment;
    }
}
