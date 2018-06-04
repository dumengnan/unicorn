package com.unicorn.data.sender.HbaseSender;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.Segment;
import com.hankcs.hanlp.seg.common.Term;
import com.unicorn.data.sender.HbaseSender.HbaseSenderService.ConvertToPut;
import org.apache.commons.configuration.CompositeConfiguration;
import org.apache.commons.configuration.Configuration;
import org.junit.Test;

public class HbaseSenderServiceTest {


    @Test
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
    public void testConvertToPut() throws Exception {
        Configuration conf = new CompositeConfiguration();
        conf.setProperty("extract.word.list", "nr,nt");
        conf.setProperty("avro.schema.dir", "test/resources");
        conf.setProperty("topics", "social_content");


        HbaseSenderService senderService = new HbaseSenderService(conf);
        ConvertToPut convertToPut = senderService.new ConvertToPut();
    }
}
