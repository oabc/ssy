DELIMITER ;
use seed;
DELIMITER //
drop PROCEDURE if exists p_commitflow;
CREATE PROCEDURE `p_commitflow`(
    serverip VARCHAR(15),
    flow text
)
label:begin
    DECLARE i int DEFAULT 1;
    DECLARE total int;
    DECLARE row VARCHAR(20);
    DECLARE port int;
    DECLARE value int;
    DECLARE price decimal(16,3) DEFAULT 0;
    DECLARE stype int DEFAULT 0;
    DECLARE error int DEFAULT 0;
    DECLARE nowtime TIMESTAMP DEFAULT NOW();
    IF(flow is NULL or LENGTH(flow)=0) THEN
        select '无效内容' as result;
        leave label;
    END IF;
    select SUBSTRING_INDEX(host,':',1) into serverip from information_schema.processlist where state='executing';
    IF(serverip is NULL or LENGTH(serverip)=0) THEN
        select '无效地址' as result;
        leave label;
    END IF;    
    select price_1g,type into price,stype from server where ip=serverip limit 1;
    IF(price=0) THEN
        select '地址异常' as result;
        leave label;
    END IF;  

    UPDATE flow_addup_auto SET flowkday=0 where TO_DAYS(lasttime)<>TO_DAYS(nowtime);
    set total = 1+(LENGTH(flow)-LENGTH(replace(flow,';','')));
        WHILE i<=total DO
                set row = REVERSE(SUBSTRING_INDEX(REVERSE(SUBSTRING_INDEX(flow,';',i)),';',1));
                set i = i+1;
                set port=SUBSTRING_INDEX(row,',',1);
                set value=SUBSTRING_INDEX(row,',',-1);
    IF(port=0 or value=0) THEN
        if(SUBSTRING_INDEX(row,',',1)<>'' or SUBSTRING_INDEX(row,',',-1)<>'') THEN
            set error = error+1;
        END IF;
    else
        insert into flow_addup_auto(ps,ip,port,value,flowk,flowkday,cost)values(concat('P',port,'T',serverip),serverip,port,value,value,value,floor(1000*price*value/1073741824)/1000) ON DUPLICATE KEY UPDATE value=flow_addup_auto.value+value,flowk=flowk+value,flowkday=flowkday+value,cost=floor(1000*flow_addup_auto.value*price/1073741824)/1000;
    END IF;
       END WHILE;
    UPDATE flow_addup_auto SET flowg=flowg+1,flowk=flowk-1073741824 where flowk>1073741824;
    UPDATE flow_addup_auto inner join user on flow_addup_auto.ip=serverip and user.port=flow_addup_auto.port and flow_addup_auto.cost>0 SET user.balance=user.balance-flow_addup_auto.cost,flow_addup_auto.value=flow_addup_auto.value-1073741824*flow_addup_auto.cost/price,flow_addup_auto.cost=0  where stype<>1 or user.day_time<nowtime;
    UPDATE flow_addup_auto inner join user on flow_addup_auto.ip=serverip and user.port=flow_addup_auto.port SET flow_addup_auto.value=0,flow_addup_auto.cost=0  where stype=1 and user.day_time>nowtime;
    IF(error>0) THEN
CREATE TABLE IF NOT EXISTS `error_log` (`id` int(11) NOT NULL auto_increment,`type` varchar(20) NOT NULL,`time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,`text` text NOT NULL,`ok` varchar(50) NOT NULL,`des` varchar(50) NOT NULL, PRIMARY KEY (id));
        insert into error_log(`type`,`des`,`text`)values('update_flow',concat('error(',error,')'),flow);
    END IF;
    select 'ok' as result;
end ;
//
DELIMITER ;
