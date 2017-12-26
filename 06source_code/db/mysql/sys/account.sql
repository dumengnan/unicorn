CREATE TABLE account(
    username varchar(100),       -- 用户名
	main_type varchar(255),      -- 大类
	sub_type  varchar(255),      -- 小类
	type varchar(20),            -- 类型(收入income 支出expense) 
	actiontime datetime,         -- 发生时间
	money double,                -- 金额
	remark varchar(255)          -- 预留备注字段
) ENGINE=InnoDB DEFAULT CHARSET=utf8;