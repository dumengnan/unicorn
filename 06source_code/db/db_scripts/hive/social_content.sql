CREATE TABLE SOCIAL_CONTENT
(
    user_id STRING,
    create_time STRING,
    status_id STRING,
    lang STRING,
    device STRING,
    retweet_count STRING,
    favorite_count STRING,
    geo STRING,
    place STRING,
    text STRING
)
CLUSTERED BY (user_id)INTO 3 BUCKETS
ROW FORMAT DELIMITED
STORED AS ORC 
TBLPROPERTIES ("transactional"="true");
