DELIMITER ;
use ssy;
DELIMITER //
drop PROCEDURE if exists p_getport;
CREATE PROCEDURE `p_getport`(
    serverip VARCHAR(15)
    ,ut VARCHAR(15)
)
begin
    DECLARE stype int DEFAULT 0;
    DECLARE nt VARCHAR(105) DEFAULT '';
    select type into stype from server where ip=serverip limit 1;
    IF exists(select port from (SELECT `port`, `password` FROM `user` WHERE (`day_time`>SYSDATE() and stype=1) OR `balance`>0 union all select port,password from user_update)as t group by port,password having count(port)=1 limit 1) THEN
        drop table if exists user_update;
        CREATE TABLE `user_update` AS SELECT `port`, `password` FROM `user` WHERE (`day_time`>SYSDATE() and stype=1) OR `balance`>0;
        insert into user_config(name,value) values ('user_update',date_format(now(),'%Y%m%d%h%i%S')) ON DUPLICATE KEY UPDATE value=date_format(now(),'%Y%m%d%h%i%s'); 
    END IF;
    select value into nt from user_config where name='user_update';
    IF nt='' THEN
        set nt=date_format(now(),'%Y%m%d%h%i%S');
        insert into user_config(`name`,`value`)values('user_update',nt);
    END IF;
    IF(nt<>ut) THEN
        select '0' as p,nt as m union select port,password from user_update;
    else
        select '0' as p,nt as m;
    END IF;     
    
end ;
//
DELIMITER ;

