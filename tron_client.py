from tronapi import HttpProvider, Tron, trx
from tronapi.utils.help import hex_to_base58
import os
import prettytable as pt
import mysql.connector
import json
from mysql.connector import errorcode
import modules.tables as tables
import sys
from modules.database_fun import *
from modules.all_class import *
from apscheduler.schedulers.background import BackgroundScheduler
from base58 import b58decode_check

'''
1. TRON大額轉帳監控
2. top DApp DAU/balance/等數據收集

transactions奇异缺失
contract信息表
'''

# Global variable

mydb = 0
cursor = 0
tron = 0
api = 0
top_list = []
data_json = {}
Max_transfer = 10 ** 12  # 默认值
Max_transfer_token = 10 ** 12


def init_config():
    # 没有配置文件,初始化一个
    _full_node = input('please input the full_node url, if you want to init config yourself,please input 666\n')
    if _full_node == '666':
        sys.exit('goodbye!')
    _solidity_node = input('please input the solidity_node url\n')
    _event_server = input('please input the event_server url\n')
    _database_host = input('please input the database_host\n')
    _database_user = input('please input the database_user\n')
    _database_password = input('please input the database_password\n')
    # maybe a more security way to store password?
    _database = input('please input the database name,like "Tron_watching"\n')
    _Max_transfer = int(input('please input the Max_transfer\n'))
    _Max_transfer_token = int(input('please input the _Max_transfer_token\n'))

    data = {
        'full_node': _full_node,
        'solidity_node': _solidity_node,
        'event_server': _event_server,
        'database': _database,
        'user': _database_user,
        'host': _database_host,
        'password': _database_password,
        'Max_transfer': _Max_transfer,
        '_Max_transfer_token': _Max_transfer_token
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
    cursor.close()

    # 建好后要连接
    mydb = mysql.connector.connect(
        user=data_json['user'],
        password=data_json['password'],
        host=data_json['host'],
        database=data_json['database']
    )
    cursor = mydb.cursor()
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
    global data_json, tron, api, mydb, Max_transfer, Max_transfer_token

    # 读取数据库配置到 data_json
    if not os.path.exists('setting.conf'):
        init_config()
    with open('setting.conf', 'r') as f:
        data_json = json.load(f)
        check = ['user', 'password', 'host', 'database', 'full_node', 'solidity_node', 'event_server', 'Max_transfer',
                 'Max_transfer_token']
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
    proxies = {
        'proxies': {
            'http': 'socks5://127.0.0.1:1080',
            'https': 'socks5://127.0.0.1:1080'
        }
    }
    full_node = HttpProvider(data_json['full_node'], )
    solidity_node = HttpProvider(data_json['solidity_node'], )
    event_server = HttpProvider(data_json['event_server'], )

    tron = Tron(full_node=full_node,
                solidity_node=solidity_node,
                event_server=event_server,
                )
    api = trx.Trx(tron)
    Max_transfer = data_json['Max_transfer']
    Max_transfer_token = data_json['Max_transfer_token']
    return True


# 清屏(等学会写UI后，这个就没用了,不过命令行还是挺hack style的:)
def clear_screen():
    os.system('cls')


def base58_to_hex(p):
    return b58decode_check(p).hex()


def analyze(new_block):
    global api, mydb, top_list
    trans = new_block.get_transactions()

    # 针对块里的每一个交易，都实例化一个类，并进行分析
    for txid, tx in trans.items():
        tx = Transaction(tx)
        txtype = tx.get_type()

        # 判断交易是否涉及TOP_APP,涉及则更新数据
        for an_app in top_list:
            i = 0
            # addresses,name,all_transaction_count,day_transaction,balance,day_users,day_transfer
            # 对应0 1 2 3 4 5 6..
            if txtype == 'TriggerSmartContract' and tx.get_contract_address() in an_app['addresses']:
                if tx.get_owner_address() not in an_app['users']:
                    top_list[i]['users'].append(tx.get_owner_address())
                top_list[i]['all_transaction_count'] += 1
                top_list[i]['day_transaction'] += 1
                top_list[i]['day_transfer'] += tx.get_call_value()

                # print(top_list[i]['day_transfer'])
                update_top_app(
                    mydb,
                    # 这里以后再改
                    top_list[i]['name'],
                    top_list[i]['all_transaction_count'],
                    top_list[i]['day_transaction'],
                    top_list[i]['balance'],
                    top_list[i]['day_transfer'],
                    top_list[i]['users']
                )
                i += 1
            else:
                i += 1
        # 4667928块已回溯
        # transfer token
        if txtype == 'TransferAssetContract' and tx.get_amount() >= Max_transfer:
            insert_transaction(mydb, tx)
            insert_big_token_transfer(mydb, tx)

        # transfer trx
        elif txtype == 'TransferContract' and tx.get_amount() >= Max_transfer_token:
            insert_transaction(mydb, tx)
            insert_big_transfer(mydb, tx)

        # transfer token by Exchange

        elif txtype == 'ExchangeTransactionContract' and tx.get_amount() >= Max_transfer_token:
            insert_transaction(mydb, tx)
            insert_big_token_transfer(mydb, tx)

        # common type
        elif txtype == 'TriggerSmartContract':
            pass
        else:
            continue
    insert_block(mydb, new_block)


def backtracking():
    global api, mydb
    # 获取今天0点时间(格林威治天文时间)
    last_block = query_last_block(mydb)
    if last_block != {}:
        last_block = Block(last_block)
        first_block = Block(query_first_block(mydb)).get_number()

    else:
        last_block = Block(api.get_current_block())
        first_block = last_block.get_number()

    yesterday = last_block.get_timestamp() - 3600 * 24

    new_block = Block(api.get_block(first_block - 2))
    # -2 是因为有可能有1块已经分析完，但没有插入数据库(意外退出造成的)
    new_first_block_time = new_block.get_timestamp()
    back_number = new_block.get_number()

    # 4646372块出现玄学bug
    # 开始回溯今天错过的块
    while new_first_block_time > yesterday:
        analyze(new_block)
        back_number -= 1
        new_block = Block(api.get_block(back_number))
        new_first_block_time = new_block.get_timestamp()
        print('{}块已回溯'.format(str(back_number + 1)))
    print('回溯完毕')


def cut_head(head_number):
    # 和analyze类似 是减去过期的数据，有时间再优化
    global mydb, api, top_list
    time_diff = Block(query_last_block(mydb)).get_timestamp() - Block(query_first_block(mydb)).get_timestamp()
    if time_diff <= 86400:
        return False
    trans = Block(api.get_block(head_number)).get_transactions()

    #

    # 针对块里的每一个交易，都实例化一个类，并进行分析
    for txid, tx in trans.items():
        tx = Transaction(tx)
        txtype = tx.get_type()

        # 判断交易是否涉及TOP_APP,涉及则更新数据
        for an_app in top_list:
            i = 0
            # addresses,name,all_transaction_count,day_transaction,balance,day_users,day_transfer
            # 对应0 1 2 3 4 5 6..
            if txtype == 'TriggerSmartContract' and tx.get_contract_address() in an_app['addresses']:

                top_list[i]['day_transaction'] -= 1
                top_list[i]['day_transfer'] -= tx.get_call_value()
                update_top_app(
                    mydb,
                    # 这里以后再改
                    top_list[i]['name'],
                    top_list[i]['all_transaction_count'],
                    top_list[i]['day_transaction'],
                    top_list[i]['balance'],
                    0,
                    top_list[i]['day_transfer']
                )
                i += 1
            else:
                i += 1
    print('             {}号块已减去'.format(head_number))
    delete_block(mydb, head_number)
    return True


def clear_dapp_users():
    global mydb
    for i in len(top_list):
        update_top_app(
            mydb,
            # 这里以后再改
            top_list[i]['name'],
            top_list[i]['all_transaction_count'],
            top_list[i]['day_transaction'],
            top_list[i]['balance'],
            top_list[i]['day_transfer'],
            []
        )


def work_begin():
    global api, mydb, top_list
    init_top_list()
    scheduler = BackgroundScheduler()
    # 每天凌晨1点清空DAU数据
    scheduler.add_job(clear_dapp_users, 'cron', hour=1)
    scheduler.start()

    if query_last_block(mydb) != {}:
        last_block = Block(query_last_block(mydb))
        first_block = Block(query_first_block(mydb))

        last_block = last_block.get_timestamp()
        first_block = first_block.get_timestamp()

        if first_block + 3600 * 24 > last_block:
            backtracking()
    else:
        backtracking()

    # 获取block_number
    last_block = Block(query_last_block(mydb))
    last_block = last_block.get_number()
    head_number = Block(query_first_block(mydb)).get_number()
    # 循环获取块信息，并解析
    while True:
        # 如果是块没更新，就再再获取，总之不能漏
        new_block = api.get_block(last_block + 1)
        if new_block == {}:
            continue
        if cut_head(head_number):
            head_number += 1
            continue

        new_block = Block(new_block)

        analyze(new_block)
        print('{}号块已解析'.format(str(last_block)))
        last_block += 1


# 初始化一个TOP_app字典，key是address, vaule是app的信息
def init_top_list():
    global mydb, top_list
    for i in query_top_app(mydb):
        tmp = {
            'addresses': i[0],
            'name': i[1],
            'all_transaction_count': i[2],
            'day_transaction': i[3],
            'balance': i[4],
            'day_transfer': i[5],
            'users': i[6]
        }
        # addresses, name, all_transaction_count, day_transaction, balance, day_users, day_transfer,users
        top_list.append(tmp)


# 查询数据库里的数据
def query_data():
    global mydb
    clear_screen()
    while True:
        chose = input(
            '''
            1.query big transfer
            2.query big transfer of token
            3.query top app information (need to get balance, just wait a while)
            4.query big transfer of token(no to_address, in most case, trade in Exchange has no to_address)
            '''
        )
        if chose == '1':
            tmp = query_big_transfer(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'owner_address', 'to_address', 'amount', 'others']
            for i in tmp:
                i[1] = hex_to_base58(i[1]).decode()
                i[2] = hex_to_base58(i[2]).decode()
                tb.add_row(i)
            print(tb)

        elif chose == '2':
            tmp = query_big_token_transfer(mydb, 1)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'asset_name', 'owner_address', 'to_address', 'amount', 'others']
            for i in tmp:
                i[1] = bytes.fromhex(i[1]).decode() if i[1] != "5f" else "trade TRX for another token"
                i[2] = hex_to_base58(i[2]).decode()
                i[3] = hex_to_base58(i[3]).decode()

                tb.add_row(i)
            print(tb)

        elif chose == '3':
            tmp = query_top_app(mydb)
            # 获取balance
            for one_app in tmp:
                addr_list = one_app[0]
                for addr_single in addr_list:
                    one_app[4] += api.get_balance(addr_single)
            tb = pt.PrettyTable()
            tb.field_names = ['addresses', 'name', 'all_transaction_count', 'day_transaction', 'balance',
                              'day_transfer', 'DAU']
            for i in tmp:
                # i[0] = hex_to_base58(i[0]).decode()
                i[0] = 'too long'
                i[6] = len(i[6])
                # i[1] = hex_to_base58(i[1]).decode()
                tb.add_row(i)
            print(tb)
        elif chose == '4':
            tmp = query_big_token_transfer(mydb, 0)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'asset_name', 'owner_address', 'amount', 'others']
            for i in tmp:
                i[2] = hex_to_base58(i[2]).decode()
                i[1] = bytes.fromhex(i[1]).decode() if i[1] != "5f" else "trade TRX for another token"
                tb.add_row(i)
            print(tb)
        else:
            clear_screen()
            print('wrong input')


# 初始化一个新的TOP_app
def set_app():
    global mydb, api

    addresses = []
    while True:
        an_address = input('please input the address of app,input 666 to quit\n')
        if an_address == '666':
            break

        an_address = base58_to_hex(an_address)
        addresses.append(an_address)
    name = input('please input the name of app\n')
    # balance = api.get_balance(address)
    top = Top(addresses, name)
    insert_top_dapp(mydb, top)


# 程序入口
def main():
    # 初始化操作，连接数据库，连接API
    if not init():
        print('init error')
        return False

    while True:
        chose = input(
            '''
            1.begin work
            2.Query data
            3.set top app(restart begin work to activate it)
            4.clear block data in database
            5.clear transactions data in database
            6.clear top_DAPP
            7.clear big transfer
            8.clear big token transfer
            '''
        )
        if chose == '1':
            work_begin()
        elif chose == '2':
            query_data()
        elif chose == '3':
            set_app()
        elif chose == '4':
            clear_block(mydb)
        elif chose == '5':
            clear_trans(mydb)
        elif chose == '6':
            clear_top_DAPP(mydb)
        elif chose == '7':
            clear_top_big_transfer(mydb)
        elif chose == '8':
            clear_top_big_token_transfer(mydb)


if __name__ == '__main__':
    main()
