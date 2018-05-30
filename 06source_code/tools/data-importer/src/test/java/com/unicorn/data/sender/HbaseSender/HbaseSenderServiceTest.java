package com.unicorn.data.sender.HbaseSender;

import com.google.common.collect.Lists;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.unicorn.data.sender.HbaseSender.HbaseSenderService.ConvertToPut;
import com.unicorn.data.sender.HbaseSender.bean.EntityValue;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Set;
import org.apache.avro.Schema;
import org.apache.avro.Schema.Parser;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import scala.Tuple2;

public class HbaseSenderServiceTest {

    private ConvertToPut convertToPut;

    @Before
    public void setUp() {
        HbaseSenderService senderService = new HbaseSenderService();

        Segment segment = HanLP.newSegment().enableNameRecognize(true).enableOrganizationRecognize(true).enablePlaceRecognize(true);
        senderService.setSegment(segment);

        List<String> extractWordList = Lists.newArrayList();
        extractWordList.add("nr");
        extractWordList.add("nt");
        senderService.setExtractWordList(extractWordList);
        this.convertToPut = senderService.new ConvertToPut();
    }

   // @Test
    public void testSplitWord() {
        String testStr = "此举旨在解决特朗普政府和全球汽车制造商长期以"
                + "来对中国进口汽车关税过高问题的抱怨。高昂的关税是福特、通用、丰田、大众"
                + "等制造商在中国建厂的原因之一，这使得中国成为世界上最大的汽车制造者。";

        System.out.println(HanLP.extractSummary(testStr, 2));
        System.out.println(HanLP.extractKeyword(testStr, 3));
        System.out.println(HanLP.extractPhrase(testStr, 3));

        String testStr2 = "2018年李书福参观了浙江大学图书馆，对浙江大学图书馆的质量提出了高度赞扬";

        Segment segment =  HanLP.newSegment().enableNameRecognize(true).enableOrganizationRecognize(true).enablePlaceRecognize(true);


        for (Term term : segment.seg(testStr2)) {
            System.out.println(term.nature.name());
        }
    }


    @Test
    public void testCreateRowKey() throws Exception {
        GenericRecord record = createSocialContentRecord();

        String rowKey = convertToPut.createRowKey(record);

        Assert.assertEquals("[\"twitter\",\"946252491401736192\"]", rowKey);
    }

    @Test
    public void parseEntityValue() {

        Set<EntityValue> result =  convertToPut.parseEntityValue("【朴槿惠要哭 二手房被冻结后检方又盯上她养老钱】12日，"
                + "围绕韩国情报机构向朴槿惠行贿一案，首尔中央地方法院  接受检方要求，批准暂时冻结她的部分个人财产，"
                + "包括一套去年购入的二手房。15日，他们再次向法院提出申请，要求冻结朴槿惠存折上的30亿韩元养老钱。16日，法院批准予以冻结");

        Assert.assertEquals(4, result.size());
    }

    @Test
    public void testConvertRecordToTuple() throws IOException {
        GenericRecord record = createSocialContentRecord();

        List<Tuple2<ImmutableBytesWritable, Put>> resultList = convertToPut.convertRecordToTuple(record);

        Assert.assertEquals(2, resultList.size());
    }


    private GenericRecord createSocialContentRecord() throws IOException {
        File avroSchemaFile = new File("src/test/resources/social_content.avsc");
        Parser parser = new Parser();
        Schema schema = parser.parse(avroSchemaFile);

        GenericRecord record = new GenericData.Record(schema);
        record.put("user_id", "913598669730979840");
        record.put("create_time", "2017-12-28 05:32:29 ");
        record.put("status_id", "946252491401736192");
        record.put("lang", "zh");
        record.put("device", "Twitter Web Client ");
        record.put("retweet_count", " 0");
        record.put("favorite_count", " 0");
        record.put("geo", "");
        record.put("text", "不知道吴淦当初哪来的勇气挑衅中国司法，好像中国法律一文不值一样，现在竟有些猪一样的队友打着美国法律的旗号帮倒忙，真应该请马克老师指点一二。 https://t.co/yOQIHRNOyE");
        record.put("screen_name", "bgger3");
        record.put("social_type", "twitter");
        record.put("crawl_time", "2018-05-07");


        return record;
    }
}
