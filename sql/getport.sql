DELIMITER ;
use seed;
DELIMITER //
drop PROCEDURE if exists p_getport;
CREATE PROCEDURE `p_getport`(
    serverip VARCHAR(15)
)
begin
    DECLARE stype int DEFAULT 0;
    select type into stype from server where ip=serverip limit 1;
    SELECT `port`, `password` FROM `user` WHERE (`day_time`>SYSDATE() and stype=1) OR `balance`>0;
end ;
//
DELIMITER ;

