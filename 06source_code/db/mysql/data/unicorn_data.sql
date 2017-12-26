
create database unicorn;
use unicorn;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for user data
-- �洢�罻ý���û��������� 
-- ----------------------------
DROP TABLE IF EXISTS `user_data`;
CREATE TABLE `user_data` (
  `ID` int(11) NOT NULL,
  `SCREEN_NAME` varchar(255) DEFAULT NULL COMMENT '�˺�',
  `NAME_STR` varchar(255) DEFAULT NULL COMMENT '�ǳ�',
  `CREATED_AT` datetime DEFAULT NULL COMMENT '����ʱ��',
  `FOLLOWERS_COUNT` int(11) DEFAULT NULL COMMENT '��˿��',
  `FRIENDS_COUNT` int(11) DEFAULT NULL COMMENT '��ע��',
  `STATUSES_COUNT` int(11) DEFAULT NULL COMMENT '״̬��',
  `SOCIAL_TYPE` varchar(255) DEFAULT NULL COMMENT '�罻ý������',
  `USER_LANG` varchar(255) DEFAULT NULL COMMENT '�û�������������',
  `UPDATE_TIME` datetime DEFAULT NULL COMMENT '��������ʱ��',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;