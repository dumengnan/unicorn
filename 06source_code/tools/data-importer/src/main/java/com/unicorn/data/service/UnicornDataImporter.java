package com.unicorn.data.service;

import org.apache.commons.cli.*;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


public class UnicornDataImporter {

    private static Logger log = LoggerFactory.getLogger(UnicornDataImporter.class);


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
        DefaultParser parser = new DefaultParser();

        return parser.parse(getOptions(), args);
    }


    public void run() throws Exception {
        SparkConf conf = new SparkConf().setAppName("UnicornDataImporter");
        JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(3));


        jssc.start();
        jssc.awaitTermination();
        jssc.stop();

    }

    public static void doMain(String[] args) {
        UnicornDataImporter dataImporter = new UnicornDataImporter();

        try {
            CommandLine line = dataImporter.parseCommandLine(args);
            if (line.hasOption("help")) {
                printUsage(getOptions());
            }

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
