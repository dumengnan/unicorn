
create database unicorn;
use unicorn;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user data
-- 存储社交媒体用户基础数据 
-- ----------------------------
DROP TABLE IF EXISTS `user_data`;
CREATE TABLE `user_data` (
  `ID` int(11) NOT NULL,
  `SCREEN_NAME` varchar(255) DEFAULT NULL COMMENT '账号',
  `NAME_STR` varchar(255) DEFAULT NULL COMMENT '昵称',
  `CREATED_AT` datetime DEFAULT NULL COMMENT '建号时间',
  `FOLLOWERS_COUNT` int(11) DEFAULT NULL COMMENT '粉丝数',
  `FRIENDS_COUNT` int(11) DEFAULT NULL COMMENT '关注数',
  `STATUSES_COUNT` int(11) DEFAULT NULL COMMENT '状态数',
  `SOCIAL_TYPE` varchar(255) DEFAULT NULL COMMENT '社交媒体类型',
  `USER_LANG` varchar(255) DEFAULT NULL COMMENT '用户所用语种类型',
  `UPDATE_TIME` datetime DEFAULT NULL COMMENT '更新数据时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;