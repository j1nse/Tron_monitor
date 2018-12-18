from tronapi import *
from tronapi import trx

proxies = {
'proxies':{
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
    }
}
full_node = HttpProvider('https://api.trongrid.io',proxies)
solidity_node = HttpProvider('https://api.trongrid.io',proxies)
event_server = HttpProvider('https://api.trongrid.io',proxies)


tron = Tron(full_node=full_node,
		solidity_node=solidity_node,
		event_server=event_server)
api=trx.Trx(tron)
# print(api.get_current_block())
# TBv7igM3eVRsd144ayw7X3ecxsAdMQfBne
print(api.get_transactions_related('TTzBSx4J2j6ZYF6YtDSGDAR7k7k7t7jMPF','to',10,0))

