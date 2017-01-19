MANAGE_PASS = 'ss233333333' 
#if you want manage in other server you should set this value to global ip
MANAGE_BIND_IP = '127.0.0.1'
#make sure this port is idle
MANAGE_PORT = 23333
config = {
    'timeout': 300, 
    'local_port': 1080, 
    'server': '0.0.0.0', 
    'server_port': 8388, 
    'local_address': '127.0.0.1', 
    'password': 'm', 
    'server_ipv6': '[::]', 
    'method': 'aes-256-cfb'
    }