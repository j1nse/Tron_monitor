import time,json
stamp = time.time()
stamp-stamp%(3600*24)
print(stamp-stamp%(3600*24))
print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(stamp-stamp%(3600*24))))
a={
	'full_node': 'https://api.trongrid.io',
        'solidity_node': 'https://api.trongrid.io',
        'event_server': 'https://api.trongrid.io',
        'database': 'tron',
        'user': 'root',
        'host': 'host',
        'password': 'root'

}
print(type(json.dumps('6')))
print(type(json.dumps(6)))
print((json.dumps('6')))
print((json.dumps('')))
