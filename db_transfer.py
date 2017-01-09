#!/usr/bin/python
# -*- coding: UTF-8 -*-

import logging
import cymysql
import time
import sys
from server_pool import ServerPool
import Config

class DbTransfer(object):

    instance = None

    def __init__(self):
        self.last_get_transfer = {}

    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance

    def push_db_all_user(self):
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

        self.last_get_transfer = curr_transfer
        query_head = 'UPDATE user'
        query_sub_when = ''
        query_sub_when2 = ''
        query_sub_in = None
        last_time = time.time()
        for id in dt_transfer.keys():
            query_sub_when += ' WHEN %s THEN u+%s' % (id, dt_transfer[id][0])
            query_sub_when2 += ' WHEN %s THEN d+%s' % (id, dt_transfer[id][1])
            if query_sub_in is not None:
                query_sub_in += ',%s' % id
            else:
                query_sub_in = '%s' % id
        if query_sub_when == '':
            return
        query_sql = query_head + ' SET u = CASE port' + query_sub_when + \
                    ' END, d = CASE port' + query_sub_when2 + \
                    ' END, t = ' + str(int(last_time)) + \
                    ' WHERE port IN (%s)' % query_sub_in
        #print query_sql
#UPDATE user SET u上传 = CASE port WHEN 10000 THEN u+79280 END, d下载 = CASE port WHEN 10000 THEN d+863188 END, t时间 = 1483353247 WHERE port IN (10000)
        conn = cymysql.connect(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, user=Config.MYSQL_USER,
                               passwd=Config.MYSQL_PASS, db=Config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()

        cur.execute(query_sql)
        cur.close()
        conn.commit()
        conn.close()


    @staticmethod
    def put_get_all(allflow):
        #数据库所有用户信息
        conn = cymysql.connect(host=Config.MYSQL_HOST, port=Config.MYSQL_PORT, user=Config.MYSQL_USER,
                               passwd=Config.MYSQL_PASS, db=Config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        serverip='127.0.0.1'
        allquery=" call p_put_get_all('%s','%s') "% (serverip,allflow)
        logging.info('dbquery[%s]' % (allquery))
        cur.execute(allquery)
        #SELECT port,passwd FROM user
        rows = []
        for r in cur.fetchall():
            rows.append(list(r))
        cur.close()
        conn.close()
        return rows
    @staticmethod
    def put_get_all_test(allflow):
        serverip='127.0.0.1'
        allquery=" call p_put_get_all('%s','%s') "% (serverip,allflow)
        logging.info('dbtestquery[%s]' % (allquery))
        #SELECT port,passwd FROM user
        rows = [[10000,'10000'],[20000,'10000'],[30000,'10000']]
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
        self.last_get_transfer = curr_transfer
        #最后一次流量等于本次流量
        allflow = ''
        for id in dt_transfer.keys():
            allflow+='%s|%s|%s,' % (id, dt_transfer[id][0], dt_transfer[id][1])#(port,up,down)
        print allflow
        
        #print query_sql
#UPDATE user SET u上传 = CASE port WHEN 10000 THEN u+79280 END, d下载 = CASE port WHEN 10000 THEN d+863188 END, t时间 = 1483353247 WHERE port IN (10000)
        #提交流量结束

        #数据库交互
        rows=DbTransfer.put_get_all_test(allflow)
        if len(rows)<1:
            return
        self.last_get_transfer = curr_transfer
        dt_alluser = {}
        #检查是否已经运行
        for row in rows:
            dt_alluser[row[0]]=row[0]
            if ServerPool.get_instance().server_is_run(row[0]) is True:
                if ServerPool.get_instance().tcp_servers_pool[row[0]]._config['password'] != row[1]:
                    #password changed
                    logging.info('db restart server at port [%s] reason: password changed' % (row[0]))
                    ServerPool.get_instance().del_server(row[0]) 
                    ServerPool.get_instance().new_server(row[0], row[1])
            else:
                logging.info('db start server at port [%s] pass [%s]' % (row[0], row[1]))
                ServerPool.get_instance().new_server(row[0], row[1])
        #检查正在运行的
        for runport in dt_transfer.keys():
            if runport not in dt_alluser.keys():
                logging.info('db restart server at port [%s] reason: password changed' % (runport))
                ServerPool.get_instance().del_server(runport)

    @staticmethod
    def del_server_out_of_bound_safe(rows):
    #停止超流量的服务
    #启动没超流量的服务
    #修改下面的逻辑要小心包含跨线程访问
        for row in rows:
            if ServerPool.get_instance().server_is_run(row[0]) is True:
                if ServerPool.get_instance().tcp_servers_pool[row[0]]._config['password'] != row[4]:
                    #password changed
                    logging.info('db restart server at port [%s] reason: password changed' % (row[0]))
                    ServerPool.get_instance().del_server(row[0]) 
                    ServerPool.get_instance().new_server(row[0], row[4])
            else:
                if row[5] == 1 and row[6] == 1 and row[1] + row[2] < row[3]:
                    logging.info('db start server at port [%s] pass [%s]' % (row[0], row[4]))
                    ServerPool.get_instance().new_server(row[0], row[4])

    @staticmethod
    def thread_db():
        import socket
        import time
        timeout = 120
        socket.setdefaulttimeout(timeout)
        while True:
            #logging.warn('db loop')
            try:
                #DbTransfer.get_instance().push_db_all_user()
                DbTransfer.get_instance().pull_db_all_user()
                #DbTransfer.del_server_out_of_bound_safe(rows)
            except Exception as e:
                logging.warn('db thread except:%s' % e)
            finally:
                time.sleep(60)

#SQLData.pull_db_all_user()
#print DbTransfer.get_instance().test()
