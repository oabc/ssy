DELIMITER ;
create database If Not Exists ssy Character Set UTF8;
use ssy;
DELIMITER //

drop table if exists user;
CREATE TABLE IF NOT EXISTS `user` (
  `username` varchar(16) NOT NULL,
  `password` varchar(16) NOT NULL,
  `port` int(8) NOT NULL,
  `day_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `balance` decimal(16,3) NOT NULL DEFAULT '0.000',
  `lastcharge` varchar(50) NOT NULL,
   PRIMARY KEY (port)
);
INSERT INTO `user` (`username`, `password`, `port`, `day_time`, `balance`, `lastcharge`) VALUES
('vvvvvv', 'qqqqqq', 6666, '2017-01-09 18:29:27', '90.379', '213456879'),
('uuu', 'qqqqqq', 8888, '2017-01-12 12:10:09', '99.969', '0'),
('yangyuxin', 'qqqqqq', 9999, '2016-12-29 08:22:14', '7.213', 'ferfiurhgeigtrg');

drop table if exists server;
CREATE TABLE IF NOT EXISTS `server` (
  `ip` varchar(16) NOT NULL,
  `price_1g` decimal(16,2) DEFAULT '0.00',
  `type` int(1) NOT NULL DEFAULT '0',
  `price_week` decimal(16,2) NOT NULL,
  `name` varchar(20) CHARACTER SET latin1 NOT NULL,
   PRIMARY KEY (ip)
);

drop table if exists user_update;
CREATE TABLE IF NOT EXISTS `user_update`(
    port int NOT NULL DEFAULT 0
    ,password varchar(20) NOT NULL DEFAULT '', PRIMARY KEY (port)); 

drop table if exists user_config;
CREATE TABLE IF NOT EXISTS `user_config`(
    name varchar(20) NOT NULL DEFAULT ''
    ,value varchar(200) NOT NULL DEFAULT '', PRIMARY KEY (name)); 

CREATE TABLE IF NOT EXISTS `user_flow_log`(
    t timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,i varchar(15) NOT NULL DEFAULT 'none'
    ,p int NOT NULL DEFAULT 0
    ,u int NOT NULL DEFAULT 0
    ,d int NOT NULL DEFAULT 0, PRIMARY KEY (t,i,p)); 

drop table if exists flow_addup_auto;
CREATE TABLE IF NOT EXISTS `flow_addup_auto`(
    ip varchar(15) NOT NULL DEFAULT '127.0.0.1'
    ,port int NOT NULL DEFAULT 0
    ,flowg bigint(20) NOT NULL DEFAULT 0,flowk int NOT NULL DEFAULT 0,flowkday int NOT NULL DEFAULT 0
    ,flowgu bigint(20) NOT NULL DEFAULT 0,flowku int NOT NULL DEFAULT 0,flowkdayu int NOT NULL DEFAULT 0
    ,flowgd bigint(20) NOT NULL DEFAULT 0,flowkd int NOT NULL DEFAULT 0,flowkdayd int NOT NULL DEFAULT 0
    ,value int NOT NULL DEFAULT 0
    ,cost decimal(16,3) NOT NULL
    ,lasttime timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    , PRIMARY KEY (ip,port)); 

//
DELIMITER ;


