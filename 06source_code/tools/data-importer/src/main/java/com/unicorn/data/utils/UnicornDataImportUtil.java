package com.unicorn.data.utils;

import java.io.File;
import org.apache.commons.configuration.CompositeConfiguration;
import org.apache.commons.configuration.Configuration;
import org.apache.commons.configuration.PropertiesConfiguration;


/**
 * Created by Administrator on 2018/3/3.
 */
public class UnicornDataImportUtil {

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

}
