import time
import sys
import thread
import pool
import Config_server

#def test():
#    thread.start_new_thread(DbTransfer.thread_db, ())
#    Api.web_server()
#    qr.peernat.com

if __name__ == '__main__':
    import utils
    config = utils.get_config(True).get('fast_open', False)
    print config
    config = utils.get_config(True).get('fast_open', False)
    print config
    if Config_server.db:
        import db_transfer
        thread.start_new_thread(db_transfer.DbTransfer.thread_db, ())
    else:
        import local_transfer
        thread.start_new_thread(local_transfer.DbTransfer.thread_db, ())
    """
    time.sleep(2)
    server_pool.ServerPool.get_instance().new_server(3333, '2333')
    while True:
        server_pool.ServerPool.get_instance().new_server(2333, '2333')
        server_pool.ServerPool.get_instance().del_server(2333)
        time.sleep(0.01)
    """
    while True:
        time.sleep(99999)
