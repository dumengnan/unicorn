package com.unicorn.data.utils;

import org.junit.Assert;
import org.junit.Test;

import java.util.Map;

/**
 * Created by Administrator on 2018/3/3.
 */
public class UnicornDataImportUtilTest {

    @Test
    public void testLoadConfig() throws Exception {
        Map<String, Object> configMap = UnicornDataImportUtil.loadConfig("src/test/resources/config.yml",
                "src/test/resources/config_override.yml");
        
        Assert.assertEquals("192.168.0.6:9000", configMap.get("kafka.brokers"));
        Assert.assertEquals("192.168.0.8_override", configMap.get("es.server"));

    }
}
