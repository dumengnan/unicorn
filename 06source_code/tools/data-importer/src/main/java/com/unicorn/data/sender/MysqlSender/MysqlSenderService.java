package com.unicorn.data.sender.MysqlSender;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import org.apache.commons.configuration.Configuration;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MysqlSenderService {
    private Logger logger = LoggerFactory.getLogger(getClass());

    private ConnectionPool connectionPool;

    private List<String> sendToMysqlTopic;

    public MysqlSenderService(Configuration configuration) throws Exception {
        String url = configuration.getString("mysql.jdbc.url");
        String username = configuration.getString("mysql.username");
        String passwd = configuration.getString("mysql.passwd");

        sendToMysqlTopic = Arrays.asList(configuration.getStringArray("send.tomysql.topics"));
        this.connectionPool = new ConnectionPool(url, username, passwd);
    }

    public void sendDataToMysql(Iterator<ConsumerRecord<String, String>> recordIterator) throws Exception {
        Connection connection = this.connectionPool.getConnection();
        try {
            connection.setAutoCommit(false);
            String insertSql = "INSERT INTO social_user (ID,SCREEN_NAME,NAME_STR,CREATED_AT,"
                    + "FOLLOWERS_COUNT,FRIENDS_COUNT,STATUSES_COUNT,SOCIAL_TYPE,USER_LANG,UPDATE_TIME)"
                    + " values (?,?,?,?,?,?,?,?,?,?)";
            PreparedStatement stat = connection.prepareStatement(insertSql);

            while(recordIterator.hasNext()) {
                ConsumerRecord<String, String> record = recordIterator.next();

                String topic = record.topic();
                String lineValue = record.value();
                String[] lineArr = lineValue.split(",");
                if (sendToMysqlTopic.contains(topic)) {
                    logger.debug("Send Data To Mysql");

                    for (int i = 0; i < lineArr.length; ++i) {
                        stat.setObject(i + 1, lineArr[i]);
                    }
                }
            }
            stat.executeBatch();
            connection.commit();
        } catch (Exception ex) {
            logger.error("Send To Mysql Exception :", ex);
        } finally {
            connection.close();
        }
    }

}
