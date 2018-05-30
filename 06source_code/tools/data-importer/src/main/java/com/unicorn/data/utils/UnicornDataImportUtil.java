package com.unicorn.data.utils;

import com.google.common.collect.Maps;
import com.unicorn.data.service.UnicornDataImporter;
import java.io.File;
import java.io.IOException;
import java.util.Map;
import org.apache.avro.Schema;
import org.apache.avro.Schema.Parser;
import org.apache.commons.configuration.CompositeConfiguration;
import org.apache.commons.configuration.Configuration;
import org.apache.commons.configuration.PropertiesConfiguration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


/**
 * Created by Administrator on 2018/3/3.
 */
public class UnicornDataImportUtil {
    private static Logger log = LoggerFactory.getLogger(UnicornDataImporter.class);

    public static Configuration loadConfig(String configFile, String configOverrideFile)
            throws Exception {
        CompositeConfiguration mergeConfig = new CompositeConfiguration();

        // 先加载override 文件
        File overrideFile = new File(configOverrideFile);
        if (overrideFile.exists()) {
            PropertiesConfiguration overrideConfig = new PropertiesConfiguration(configOverrideFile);
            mergeConfig.addConfiguration(overrideConfig);
        }

        PropertiesConfiguration config = new PropertiesConfiguration(configFile);
        mergeConfig.addConfiguration(config);

        return mergeConfig;
    }

    public static Map<String, Schema> loadAvroSchemaFromFile(String avroSchemaDir, String[] topicList) throws IOException {
        Map<String, Schema> schemaMap = Maps.newHashMap();

        for (String topic : topicList) {
            File avroSchemaFile = new File(avroSchemaDir, topic + UnicornConstant.SCHMEA_FILE_PREFIX);
            if (!avroSchemaFile.exists()) {
                log.error("Topic {} Avro File {} Not Exists!", topic, avroSchemaFile.getAbsolutePath());
            }

            Parser parser = new Parser();
            Schema schema = parser.parse(avroSchemaFile);

            schemaMap.put(topic, schema);
        }

        return schemaMap;
    }

}
