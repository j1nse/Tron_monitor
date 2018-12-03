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
tron.default_block = 'latest'
api=trx.Trx(tron)
#print(api.get_current_block())
print(api.get_block(4624423))
