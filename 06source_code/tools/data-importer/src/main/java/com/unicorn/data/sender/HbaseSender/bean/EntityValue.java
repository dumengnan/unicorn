package com.unicorn.data.sender.HbaseSender.bean;

import java.util.Objects;

/**
 * 存储在hbase entity family 中的数据结构.
 * Created by Administrator on 2018/5/26.
 */
public class EntityValue {
    private String value;
    private String type;

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

    @Override
    public boolean equals(Object obj) {
        if (obj == null) return false;
        if (getClass() != obj.getClass()) return false;
        final EntityValue other = (EntityValue) obj;
        return Objects.equals(this.type, other.type)
                && Objects.equals(this.type, other.type);
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.type, this.value);
    }
}
