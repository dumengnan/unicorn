package com.unicorn.data.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class UnicornDataImporter {

    private static Logger log = LoggerFactory.getLogger(UnicornDataImporter.class);

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
