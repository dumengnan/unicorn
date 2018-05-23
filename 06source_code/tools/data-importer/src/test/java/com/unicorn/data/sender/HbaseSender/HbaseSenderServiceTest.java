package com.unicorn.data.sender.HbaseSender;

import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;
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
        for (Term term : HanLP.segment(testStr)) {
            System.out.println(term.word);
        }

    }
}
