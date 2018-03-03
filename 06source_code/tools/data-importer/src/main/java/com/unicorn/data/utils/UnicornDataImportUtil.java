package com.unicorn.data.utils;

import com.google.common.collect.Maps;
import org.yaml.snakeyaml.Yaml;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;

/**
 * Created by Administrator on 2018/3/3.
 */
public class UnicornDataImportUtil {

    public static Map<String, Object> loadConfig(String yamlConfig, String overrideYamlConfig)
            throws IOException {
        Map<String, Object> configMap = Maps.newHashMap();
        Yaml yaml = new Yaml();

        File yamlFile = new File(yamlConfig);
        if (yamlFile.exists()) {
            try (InputStream in = Files.newInputStream(Paths.get(yamlConfig))) {
                Map<String, Object> result = yaml.load(in);
                configMap.putAll(result);
            }
        }

        File overrideFile = new File(overrideYamlConfig);
        if (overrideFile.exists()) {
            try (InputStream in = Files.newInputStream(Paths.get(overrideYamlConfig))) {
                Map<String, Object> overrideResult = yaml.load(in);
                configMap.putAll(overrideResult);
            }
        }

        return configMap;
    }

}
