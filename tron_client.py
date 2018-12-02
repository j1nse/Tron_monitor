from tronapi import *
from tronapi import trx
import os
import prettytable as pt
from solc import compile_source
import mysql.connector
from mysql.connector import errorcode
import json
import tables
import sys
from database_fun import *
from all_class import *

'''
1. TRON大額轉帳監控
2. top DApp DAU/balance/等數據收集
'''

# Global variable
mydb = 0
cursor = 0
tron = 0
api = 0
top_list = {}
data_json = {}
Max_transfer = 0
Max_transfer_token = 0


def init_config():

    # 没有配置文件,初始化一个
    _full_node = input('please input the full_node url, if you want to init config yourself,please input 666')
    if _full_node == '666':
        sys.exit('goodbye!')
    _solidity_node = input('please input the solidity_node url')
    _event_server = input('please input the event_server url')
    _database_host = input('please input the database_host')
    _database_user = input('please input the database_user')
    _database_password = input('please input the database_password')
    # maybe a more security way to store password?
    _database = input('please input the database name,like "Tron_watching"')

    data = {
        'full_node': _full_node,
        'solidity_node': _solidity_node,
        'event_server': _event_server,
        'database': _database,
        'user': _database_user,
        'host': _database_host,
        'password': _database_password
    }
    with open('setting.conf', 'w+') as f:
        json.dump(data, f)


def init_create_db():
    global data_json, mydb, cursor

    # 建库
    mydb = mysql.connector.connect(
        user=data_json['user'],
        password=data_json['password'],
        host=data_json['host']
    )
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE {}".format(data_json['database']))

    # 批量建表
    for table_name in tables._tables:
        table_description = tables._tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def init():
    global data_json, tron, api, mydb

    # 读取数据库配置到 data_json
    if not os.path.exists('setting.conf'):
        init_config()
    with open('setting.conf', 'r') as f:
        data_json = json.load(f)
        check = ['user', 'password', 'host', 'database', 'full_node', 'solidity_node', 'event_server']
        for i in check:
            if i not in data_json:
                return False

    # 连接数据库
    try:
        mydb = mysql.connector.connect(
            user=data_json['user'],
            password=data_json['password'],
            host=data_json['host'],
            database=data_json['database']
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist,just create a new database, please restart program")
            init_create_db()
            return False
        else:
            print(err)
            return False

    # 连接API(http)
    tron = Tron(full_node=data_json['full_node'],
                solidity_node=data_json['solidity_node'],
                event_server=data_json['event_server']
                )
    tron.default_block = 'latest'
    api = trx.Trx(tron)

    return True


# 清屏(等学会写UI后，这个就没用了,不过命令行还是挺hack style的:)
def clear_screen():
    os.system('cls')


def work_begin():
    global api, mydb, top_list
    last_block = ''
    init_top_list()

    # 循环获取块信息，并解析
    while True:

        # 如果是块没更新，就再跳过，总之不能漏
        new_block = Block(api.get_current_block())
        if last_block == new_block.get_number():
            continue
        else:
            last_block = new_block.get_number()
        trans = new_block.get_transactions()

        # 针对块里的每一个交易，都实例化一个类，并进行分析
        for txid, tx in trans.iteritems():
            tx = Transaction(tx)
            txtype = tx.get_type()

            # 判断交易是否涉及TOP_APP,涉及则更新数据
            if tx.get_contract_address() in top_list:
                top_list[tx.get_contract_address()]['all_transaction_count'] += 1
                top_list[tx.get_contract_address()]['day_transaction'] += 1
                top_list[tx.get_contract_address()]['balance'] = api.get_balance(tx.get_contract_address())
                # 这里或许可以优化一下？不知道一直操作数据库会不会不太好，但是不这样程序意外退出可能造成数据丢失
                update_top_app(
                    mydb,
                    tx.get_contract_address(),
                    top_list[tx.get_contract_address()]['all_transaction_count'],
                    top_list[tx.get_contract_address()]['day_transaction'],
                    top_list[tx.get_contract_address()]['balance']
                )

            # transfer token
            if txtype == 'TransferAssetContract':
                insert_transaction(mydb, tx)
                if tx.get_amount() >= Max_transfer:
                    insert_big_transfer(mydb, tx)

            # transfer trx
            elif txtype == 'TransferContract':
                insert_transaction(mydb, tx)
                if tx.get_amount() >= Max_transfer_token:
                    insert_big_token_transfer(mydb, tx)

            # transfer trx by Exchange
            elif txtype == 'ExchangeTransactionContract':
                insert_transaction(mydb, tx)
                if tx.get_amount() >= Max_transfer_token:
                    insert_big_token_transfer(mydb, tx)

            # common type
            elif txtype == 'TriggerSmartContract':
                pass
            else:
                continue


# 初始化一个TOP_app字典，key是address, vaule是app的信息
def init_top_list():
    global mydb, top_list
    for i in query_top_app(mydb):
        top_list[i['address']] = i


# 查询数据库里的数据
def query_data():
    global mydb
    clear_screen()
    while True:
        chose = input(
            '''
            1.query big transfer
            2.query big transfer of token
            3.query top app information     
            '''
        )
        if chose == '1':
            tmp = query_big_transfer(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'owner_address', 'to_address', 'amount', 'others']
            for i in tmp:
                tb.add_row(i)
            print(tb)

        elif chose == '2':
            tmp = query_big_token_transfer(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'asset_name', 'owner_address', 'to_address', 'amount', 'others']
            for i in tmp:
                tb.add_row(i)
            print(tb)

        elif chose == '3':
            tmp = query_top_app(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['address', 'all_transaction_count', 'day_transaction', 'balance']
            for i in tmp:
                tb.add_row(i)
            print(tb)
        else:
            clear_screen()
            print('wrong input')


# 初始化一个新的TOP_app
def set_app():
    global mydb, api
    address = input('please input the address of app')
    balance = api.get_balance(address)
    top = Top(address, 0, 0, balance)
    insert_top_DAPP(mydb, top)


# 程序入口
def main():
    # 初始化操作，连接数据库，连接API
    if not init():
        print('init error')
        return False

    chose = input(
        '''
        1.begin work
        2.Query data
        3.set top app(restart begin work to activate it)
        4.clear block data in database
        '''
    )
    while True:
        if chose == '1':
            work_begin()
        elif chose == '2':
            query_data()
        elif chose == '3':
            set_app()
        elif chose == '4':
            pass


if __name__ == '__main__':
    main()
