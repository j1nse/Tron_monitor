#coding:utf-8
from tronapi import HttpProvider, Tron
full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = 'https://api.trongrid.io'
tron = Tron()
tron.default_block = 'latest'
tron.get_block('latest')