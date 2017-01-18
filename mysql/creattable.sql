    CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(32) NOT NULL,
  `pass` varchar(16) NOT NULL,
  `passwd` varchar(16) NOT NULL,
  `t` int(11) NOT NULL DEFAULT '0',
  `u` bigint(20) NOT NULL,
  `d` bigint(20) NOT NULL,
  `transfer_enable` bigint(20) NOT NULL,
  `port` int(11) NOT NULL,
  `switch` tinyint(4) NOT NULL DEFAULT '1',
  `enable` tinyint(4) NOT NULL DEFAULT '1',
  `type` tinyint(4) NOT NULL DEFAULT '1',
  `last_get_gift_time` int(11) NOT NULL DEFAULT '0',
  `last_rest_pass_time` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`,`port`)
) ENGINE=InnoDB AUTO_INCREMENT=415 DEFAULT CHARSET=utf8;

用户信息更新表

DELIMITER ;
use seed;
DELIMITER //

drop table user_update;
CREATE TABLE IF NOT EXISTS `user_update`(
    port int NOT NULL DEFAULT 0
    ,password varchar(20) NOT NULL DEFAULT '', PRIMARY KEY (port)); 

drop table user_config;
CREATE TABLE IF NOT EXISTS `user_config`(
    name varchar(20) NOT NULL DEFAULT ''
    ,value varchar(200) NOT NULL DEFAULT '', PRIMARY KEY (name)); 

drop table flow_addup_auto;
CREATE TABLE IF NOT EXISTS `flow_addup_auto`(
    ip varchar(15) NOT NULL DEFAULT '127.0.0.1',port int NOT NULL DEFAULT 0
    ,flowg bigint(20) NOT NULL DEFAULT 0,flowk int NOT NULL DEFAULT 0,flowkday int NOT NULL DEFAULT 0
    ,flowgu bigint(20) NOT NULL DEFAULT 0,flowku int NOT NULL DEFAULT 0,flowkdayu int NOT NULL DEFAULT 0
    ,flowgd bigint(20) NOT NULL DEFAULT 0,flowkd int NOT NULL DEFAULT 0,flowkdayd int NOT NULL DEFAULT 0
    ,value int NOT NULL DEFAULT 0,cost decimal(16,3) NOT NULL,lasttime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (ip,port)); 

//
DELIMITER ;


流量表
