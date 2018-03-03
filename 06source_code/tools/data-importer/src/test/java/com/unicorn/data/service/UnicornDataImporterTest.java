package com.unicorn.data.service;


import org.apache.commons.cli.CommandLine;
import org.junit.Assert;
import org.junit.Test;

import java.util.Properties;

public class UnicornDataImporterTest {

  @Test
  public void testGetOptions() throws Exception {
    String[] args = {"-Dkey1=value1", "-Dkey2=value2"};

    UnicornDataImporter dataImporter = new UnicornDataImporter();

    CommandLine line = dataImporter.parseCommandLine(args);

    Properties commandProp = line.getOptionProperties("D");

    Assert.assertEquals("value1", commandProp.getProperty("key1"));
    Assert.assertEquals("value2", commandProp.getProperty("key2"));
  }
}
