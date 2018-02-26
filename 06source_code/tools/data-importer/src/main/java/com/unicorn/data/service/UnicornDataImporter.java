package com.unicorn.data.service;

import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
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


    public static void doMain(String[] args) {

    }

    public static void main(String[] args) {
        try {
            doMain(args);
        } catch (Exception ex) {
            log.error("Data Importer Exception ", ex);
        }
    }
}