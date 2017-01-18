#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import cymysql
import time
import sys
from server_pool import ServerPool
import Config
import user

class DbTransfer(object):

    instance = None

    def __init__(self):
        self.port_passwd=user.PORT_PASSWD
        self.last_get_transfer = {}
        self.last_get_dbtime ='1'
        self.loopfloortime =0
    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance

    @staticmethod
    def put_get_all(last_get_time,allflow):
        #数据库所有用户信息
        conn = cymysql.connect(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, user=Config.MYSQL_USER,
                               passwd=Config.MYSQL_PASS, db=Config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        allquery="call p_put_get_all('%s','%s')"% (last_get_time,allflow)
        logging.info('dbquery:%s' % (allquery))
        cur.execute(allquery)
        #SELECT port,passwd FROM user
        rows = []
        for r in cur.fetchall():
            rows.append(list(r))
        cur.close()
        if len(rows)>0:
            conn.commit()
        conn.close()
        return rows
    def pull_db_all_user(self):

        #更新用户流量到数据库
        last_transfer = self.last_get_transfer
        curr_transfer = ServerPool.get_instance().get_servers_transfer()
        #上次和本次的增量
        dt_transfer = {}
        for id in curr_transfer.keys():
            if id in last_transfer:
                if last_transfer[id][0] == curr_transfer[id][0] and last_transfer[id][1] == curr_transfer[id][1]:
                    continue
                elif curr_transfer[id][0] == 0 and curr_transfer[id][1] == 0:
                    continue
                elif last_transfer[id][0] <= curr_transfer[id][0] and \
                last_transfer[id][1] <= curr_transfer[id][1]:
                    dt_transfer[id] = [curr_transfer[id][0] - last_transfer[id][0],
                                       curr_transfer[id][1] - last_transfer[id][1]]
                else:
                    dt_transfer[id] = [curr_transfer[id][0], curr_transfer[id][1]]
            else:
                if curr_transfer[id][0] == 0 and curr_transfer[id][1] == 0:
                    continue
                dt_transfer[id] = [curr_transfer[id][0], curr_transfer[id][1]]
        #最后一次流量等于本次流量
        if len(dt_transfer)<1 and len(curr_transfer)>0:
            self.loopfloortime=self.loopfloortime+1
            if self.loopfloortime<30:
                logging.info('floortime:%s'%self.loopfloortime)
                return
        allflow = ''
        self.loopfloortime=0
        for id in dt_transfer.keys():
            allflow+='%s|%s|%s,' % (id, dt_transfer[id][0], dt_transfer[id][1])#(port,up,down)
        logging.info('flow(%s)'%allflow)
        #print query_sql
#UPDATE user SET u上传 = CASE port WHEN 10000 THEN u+79280 END, d下载 = CASE port WHEN 10000 THEN d+863188 END, t时间 = 1483353247 WHERE port IN (10000)
        #提交流量结束

        #数据库交互

        if len(self.port_passwd)>1:
            rows=self.port_passwd
        else
            rows=DbTransfer.put_get_all(self.last_get_dbtime,allflow)


        if len(rows)<1 or '%s'%rows[0][0]<>'0':
            logging.info('userinfo PUT AND GET error.')
            return            
        self.last_get_transfer = curr_transfer
        _passwd='%s'%rows[0][1]
        logging.info('dbtime[%s][%s](%s,%s)'%(self.last_get_dbtime==_passwd,len(rows),self.last_get_dbtime,_passwd))
        if len(rows)==1 and self.last_get_dbtime==_passwd:
            return
        self.last_get_dbtime=_passwd    
        del rows[0]
        dt_alluser = {}
        #检查是否已经运行
        for row in rows:
            _port=int(row[0])
            _passwd='%s'%row[1]
            dt_alluser[_port]=_port            
            if _port in curr_transfer.keys():
                if ServerPool.get_instance().tcp_servers_pool[_port]._config['password'] !=_passwd:
                    #password changed
                    logging.info('restart on changed password(%s=>%s)' %(_port,_passwd))
                    ServerPool.get_instance().del_server(_port) 
                    time.sleep(3)
                    ServerPool.get_instance().new_server(_port, _passwd)
            else:
                logging.info('new port(%s=>%s)' % (_port, _passwd))
                ServerPool.get_instance().new_server(_port, _passwd)
        #检查正在运行的
        for runport in curr_transfer.keys():
            if runport not in dt_alluser.keys():
                logging.info('run to stop(%s)' % (runport))
                ServerPool.get_instance().del_server(runport)

    @staticmethod
    def thread_db():
        import socket
        import time
        timeout = 120
        socket.setdefaulttimeout(timeout)
        while True:
            #logging.warn('db loop')
            DbTransfer.get_instance().pull_db_all_user()
            try:
                d=5
                #DbTransfer.get_instance().pull_db_all_user()
            except Exception as e:
                logging.warn('db thread except:%s' % e)
            finally:
                #time.sleep(60)
                time.sleep(10)

#SQLData.pull_db_all_user()
#print DbTransfer.get_instance().test()
