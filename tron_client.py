from tronapi import *
from tronapi import trx
from solc import compile_source
import mysql.connector
import json
import tables

full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')


tron = Tron(full_node=full_node,
        solidity_node=solidity_node,
        event_server=event_server)
tron.default_block = 'latest'
a=trx.Trx(tron)
#print(a.get_current_block())

	
mycursor = mydb.cursor()
def insert_block_db(block):
	mycursor
	
def init_cofig():
	# 没有配置文件,初始化一个
	_full_node = input('please input the full_node url')
	_solidity_node = input('please input the solidity_node url')
	_event_server = input('please input the event_server url')
	_database_name = input('please input hte database name,like "Tron_watching"')
	data = {
		'full_node':_full_node,
		'solidity_node':_solidity_node,
		'event_server':_event_server,
		'database_name':_database_name
	}
	with open('setting.conf', 'w+') as f:
		json.dump(data, f)


def init_create_table():
	# 批量初始化表
	for table_name in _tables:
	    table_description = _tables[table_name]
	    try:
	        print("Creating table {}: ".format(table_name),end='')
	        mycursor.execute(table_description)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")

def init():
	# 读取数据库配置到 data_json
	try:
		with open('setting.conf','r') as f:
			data_json = json.load(f)
	except FileNotFoundError:
		init_config()
	
	# 连接数据库
	try:
		mydb = mysql.connector.connect(database_json)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
			return 0
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
			return 0
		else:
			print(err)
			return 0


	



