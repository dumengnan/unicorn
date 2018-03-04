package com.unicorn.data.utils;

import java.util.List;
import org.apache.commons.configuration.Configuration;
import org.junit.Assert;
import org.junit.Test;

import java.util.Map;

/**
 * Created by Administrator on 2018/3/3.
 */
public class UnicornDataImportUtilTest {

    @Test
    public void testLoadConfigOverride() throws Exception {
        Configuration config = UnicornDataImportUtil
                .loadConfig("src/test/resources/config.properties",
                        "src/test/resources/config_override.properties");

        Assert.assertEquals("192.168.0.6:9000", config.getString("kafka.brokers"));
        Assert.assertEquals("192.168.0.8_override", config.getString("es.server"));
    }

    @Test
    public void testLoadConfigNoOverride() throws Exception {
        Configuration config = UnicornDataImportUtil
                .loadConfig("src/test/resources/config.properties",
                        "src/test/resources/config2_override.properties");

        Assert.assertEquals("192.168.0.6:9000", config.getString("kafka.brokers"));
        Assert.assertEquals("192.168.0.7", config.getString("hbase.server"));
    }

    @Test
    public void testLoadConfigList() throws Exception {
        Configuration config = UnicornDataImportUtil
                .loadConfig("src/test/resources/config.properties",
                        "src/test/resources/config2_override.properties");

        Assert.assertEquals(3, config.getStringArray("send.tomysql.topics").length);

        List topicList = config.getList("send.tomysql.topics");
        Assert.assertEquals(3, topicList.size());
    }
}
