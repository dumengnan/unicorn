package com.unicorn.data.service;

import com.google.common.collect.Maps;
import com.unicorn.data.sender.HbaseSender.HbaseSenderService;
import com.unicorn.data.utils.UnicornConstant;
import com.unicorn.data.utils.UnicornDataImportUtil;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Map;
import java.util.Properties;
import org.apache.commons.cli.*;
import org.apache.commons.configuration.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.mapreduce.TableOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.SparkConf;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class UnicornDataImporter {

    private static Logger log = LoggerFactory.getLogger(UnicornDataImporter.class);

    private Properties consumerProperties;

    private Configuration applicationConfig;

    private static void printUsage(Options options) {
        final HelpFormatter formatter = new HelpFormatter();
        formatter.printHelp("UnicornDataImporter", options);
    }

    public static Options getOptions() {
        Option help = new Option("h", "the command help");

        // 此处定义参数类似于 java 命令中的 -D<name>=<value>
        Option property = OptionBuilder.withArgName("property=value")
                .hasArgs(2).withValueSeparator().withDescription(
                        "search the objects which have the target property and value").create("D");
        Options opts = new Options();
        opts.addOption(help);
        opts.addOption(property);

        return opts;
    }

    CommandLine parseCommandLine(String[] args) throws Exception {
        CommandLineParser  parser = new PosixParser();

        return parser.parse(getOptions(), args);
    }

    public void readConf() throws Exception {
        consumerProperties.load(new FileInputStream("etc/consumer.properties"));

        applicationConfig = UnicornDataImportUtil
                .loadConfig("etc/config.properties", "etc/config_override.properties");

    }

    public void run() throws Exception {
        SparkConf conf = new SparkConf().setAppName("UnicornDataImporter");
        JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(3));

        Map<String, Object> kafkaParams = Maps.newHashMap((Map) consumerProperties);
        kafkaParams.put("bootstrap.servers", applicationConfig.getString("bootstrap.servers"));
        String[] topicList = applicationConfig.getStringArray("topics");

        JavaInputDStream<ConsumerRecord<String, byte[]>> stream = KafkaUtils.createDirectStream(jssc,
                LocationStrategies.PreferConsistent(), ConsumerStrategies.<String, byte[]>Subscribe(
                        Arrays.asList(topicList), kafkaParams));

        org.apache.hadoop.conf.Configuration hbaseConf = getHbaseConf();
        HbaseSenderService hbaseSenderService = new HbaseSenderService(applicationConfig);
        stream.foreachRDD(rdd -> {
                    rdd.flatMapToPair(hbaseSenderService.new ConvertToPut()).saveAsNewAPIHadoopDataset(hbaseConf);
                }
        );

        jssc.start();
        jssc.awaitTermination();
        jssc.stop();
    }


    private org.apache.hadoop.conf.Configuration getHbaseConf() throws IOException {
        String hbaseZkServer = applicationConfig.getString("hbase.zookeeper.server");
        String hbaseZkPort = applicationConfig.getString("hbase.zookeeper.port");
        org.apache.hadoop.conf.Configuration hbaseConf = HBaseConfiguration.create();

        hbaseConf.set("hbase.zookeeper.quorum", hbaseZkServer);
        hbaseConf.set("hbase.zookeeper.property.clientPort", hbaseZkPort);

        Job newApiJobConf = Job.getInstance(hbaseConf);
        newApiJobConf.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE,
                UnicornConstant.CONTENT_TABLE);
        newApiJobConf.setOutputFormatClass(TableOutputFormat.class);

        return hbaseConf;
    }

    public static void doMain(String[] args) {
        UnicornDataImporter dataImporter = new UnicornDataImporter();

        try {
            CommandLine line = dataImporter.parseCommandLine(args);
            if (line.hasOption("help")) {
                printUsage(getOptions());
            }

            dataImporter.readConf();
            dataImporter.run();
        } catch (Exception ex) {
            log.error(" ", ex);
        }
    }

    public static void main(String[] args) {
        try {
            doMain(args);
        } catch (Exception ex) {
            log.error("Data Importer Exception ", ex);
        }
    }
}
