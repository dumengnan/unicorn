package com.unicorn.data.sender.HbaseSender.bean;

/**
 * 存储在hbase entity family 中的数据结构.
 * Created by Administrator on 2018/5/26.
 */
public class EntityValue {
    private String type;
    private String value;

    public EntityValue(String type, String value) {
        this.type = type;
        this.value = value;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
