package com.unicorn.data.sender.MysqlSender;

import java.sql.Connection;
import javax.sql.DataSource;
import org.apache.commons.dbcp.ConnectionFactory;
import org.apache.commons.dbcp.DriverManagerConnectionFactory;
import org.apache.commons.dbcp.PoolableConnectionFactory;
import org.apache.commons.dbcp.PoolingDataSource;
import org.apache.commons.pool.impl.GenericObjectPool;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ConnectionPool {

    private Logger logger = LoggerFactory.getLogger(getClass());

    private static final String MYSQL_DRIVER_CLASS = "com.mysql.jdbc.Driver";

    private DataSource dataSource;
    private static GenericObjectPool gPool;

    public ConnectionPool(String connectionUrl, String userName, String passWd) throws Exception {
        this.dataSource = setUpPool(connectionUrl, userName, passWd);
    }

    private DataSource setUpPool(String connectionUrl, String userName, String passWd)
            throws Exception {
        Class.forName(MYSQL_DRIVER_CLASS);

        // Creates an Instance of GenericObjectPool That Holds Our Pool of Connections Object!
        gPool = new GenericObjectPool();
        gPool.setMaxActive(5);

        // Creates a ConnectionFactory Object Which Will Be Use by the Pool to Create the Connection Object!
        ConnectionFactory cf = new DriverManagerConnectionFactory(connectionUrl, userName, passWd);

        // Creates a PoolableConnectionFactory That Will Wraps the Connection Object Created by the ConnectionFactory to Add Object Pooling Functionality!
        PoolableConnectionFactory pcf = new PoolableConnectionFactory(cf, gPool, null, null, false,
                true);
        return new PoolingDataSource(gPool);
    }

    public Connection getConnection() throws Exception {
        return this.dataSource.getConnection();
    }

    public void close() throws Exception {
        this.gPool.close();
    }

}
