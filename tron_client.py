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

'''

# Global variable
mydb = 0
api = 0
top_list = []
data_json = {}
Max_transfer = 10 ** 12  # 默认值
Max_transfer_token = 10 ** 12
common_type = [
    'TriggerSmartContract',
    'TransferAssetContract',
    'TransferContract',
    'ExchangeTransactionContract',
    'VoteWitnessContract',
    'FreezeBalanceContract',
    'UnfreezeBalanceContract'
]


# 没有配置文件,初始化一个
def init_config():
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
        'Max_transfer_token': _Max_transfer_token
    }
    with open('setting.conf', 'w+') as f:
        json.dump(data, f)


# 建库，建表函数
def init_create_db():
    global data_json, mydb

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


# 初始化函数，用于读取配置文件，连接数据库，连接API
def init():
    global data_json, api, mydb, Max_transfer, Max_transfer_token

    # 读取数据库配置到 data_json, 若不存在配置文件则建一个
    if not os.path.exists('setting.conf'):
        init_config()
    with open('setting.conf', 'r') as f:
        data_json = json.load(f)
        # 检查需要的参数全了没
        check = ['user', 'password', 'host', 'database', 'full_node', 'solidity_node', 'event_server', 'Max_transfer',
                 'Max_transfer_token', 'proxy']
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
            # 如果数据库不存在，就建
            init_create_db()
            return False
        else:
            print(err)
            return False

    # 判断代理
    if data_json['proxy'].strip() != '':
        proxy = {
            'proxies': {
                'http': data_json['proxy'],
                'https': data_json['proxy']
            }
        }
    else:
        proxy = {}
    # 连接API(http)
    full_node = HttpProvider(data_json['full_node'], proxy)
    solidity_node = HttpProvider(data_json['solidity_node'], proxy)
    event_server = HttpProvider(data_json['event_server'], proxy)

    tron = Tron(full_node=full_node,
                solidity_node=solidity_node,
                event_server=event_server,
                )
    api = trx.Trx(tron)
    Max_transfer = data_json['Max_transfer']
    Max_transfer_token = data_json['Max_transfer_token']
    return True


# 清屏(命令行还是挺hack style的:)
def clear_screen():
    os.system('cls')


# 很明显的函数
def base58_to_hex(p):
    return b58decode_check(p).hex()


# 用来解析得到的块的信息的函数
def analyze(new_block):
    global api, mydb, top_list
    trans = new_block.get_transactions()

    # 针对块里的每一个交易，都实例化一个交易类，并进行分析
    for txid, tx in trans.items():
        tx = Transaction(tx)
        txtype = tx.get_type()

        # 判断交易是否涉及TOP_APP,涉及则更新数据
        for an_app in top_list:
            i = 0
            # an_app 是字典，key为 addresses,name,all_transaction_count,day_transaction,balance,day_transfer,users
            if txtype == 'TriggerSmartContract' and tx.get_contract_address() in an_app['addresses']:
                # 如果是新用户，就加入
                if tx.get_owner_address() not in an_app['users']:
                    top_list[i]['users'].append(tx.get_owner_address())
                top_list[i]['all_transaction_count'] += 1
                top_list[i]['day_transaction'] += 1
                top_list[i]['day_transfer'] += tx.get_call_value()

                # update的参数 name, all_transaction_count, day_transaction, balance, day_transfer, users
                update_top_app(
                    mydb,
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

        elif txtype == 'VoteWitnessContract':
            insert_vote(mydb, tx)

        elif txtype == 'FreezeBalanceContract' or txtype == 'UnfreezeBalanceContract':
            insert_freeze(mydb, tx)

        # rare type
        elif txtype not in common_type:
            insert_other(mydb, tx)

    # 插入块到数据库，表示分析完了
    insert_block(mydb, new_block)


# 往前回溯块
def backtracking():
    global api, mydb
    last_block = query_last_block(mydb)

    # 如果是空的，就从现在开始回溯,否则从最前面的块开始回溯
    if last_block != {}:
        last_block = Block(last_block)
        first_block = Block(query_first_block(mydb)).get_number()

    else:
        last_block = Block(api.get_current_block())
        first_block = last_block.get_number()

    # 要回溯到的时间点
    yesterday = last_block.get_timestamp() - 3600 * 24

    new_block = Block(api.get_block(first_block - 2))
    # -2 是因为有可能有1块已经分析完，但没有插入数据库(意外退出造成的),防止插入相同数据导致错误
    new_first_block_time = new_block.get_timestamp()
    back_number = new_block.get_number()

    # 4646372块会出现玄学bug
    # 开始回溯今天错过的块
    while new_first_block_time > yesterday:
        analyze(new_block)
        back_number -= 1
        new_block = Block(api.get_block(back_number))
        new_first_block_time = new_block.get_timestamp()
        print('{}块已回溯'.format(str(back_number + 1)))
    print('回溯完毕')


# 和analyze类似 是减去过期的数据
def cut_head(head_number):
    global mydb, api, top_list

    # 查看是否有过期的块, 86400 == 24 * 3600
    time_diff = Block(query_last_block(mydb)).get_timestamp() - Block(query_first_block(mydb)).get_timestamp()
    if time_diff <= 86400:
        return False
    trans = Block(api.get_block(head_number)).get_transactions()

    # 针对块里的每一个交易，都实例化一个类，并进行分析
    for txid, tx in trans.items():
        tx = Transaction(tx)
        txtype = tx.get_type()

        # 判断交易是否涉及TOP_APP,涉及则更新数据
        for an_app in top_list:
            i = 0  # top_list里第i个app
            # an_app 是字典，key为 addresses,name,all_transaction_count,day_transaction,balance,day_transfer,users
            if txtype == 'TriggerSmartContract' and tx.get_contract_address() in an_app['addresses']:

                top_list[i]['day_transaction'] -= 1
                top_list[i]['day_transfer'] -= tx.get_call_value()
                # update的参数 name, all_transaction_count, day_transaction, balance, day_transfer, users
                update_top_app(
                    mydb,
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
    print('             {}号块已减去'.format(head_number))
    # 从数据库删除这个块
    delete_block(mydb, head_number)
    return True


# 清理dapp的users信息
def clear_dapp_users():
    global mydb
    for i in len(top_list):
        update_top_app(
            mydb,
            top_list[i]['name'],
            top_list[i]['all_transaction_count'],
            top_list[i]['day_transaction'],
            top_list[i]['balance'],
            top_list[i]['day_transfer'],
            []  # 这里为空，即为清除
        )


# 用于回溯未同步块，分析块信息，同步最新块
def work_begin():
    global api, mydb, top_list
    # 初始化dapp的信息到全局变量里
    init_top_list()

    # 每天凌晨1点清空DAU数据
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_dapp_users, 'cron', hour=1)
    scheduler.start()

    # 如果最早的块和最晚的块之间差不到1天，就要回溯；或者库里没有块信息，也要回溯
    if query_last_block(mydb) != {}:
        last_block = Block(query_last_block(mydb))
        first_block = Block(query_first_block(mydb))

        last_block = last_block.get_timestamp()
        first_block = first_block.get_timestamp()

        if first_block + 3600 * 24 > last_block:
            backtracking()
    else:
        backtracking()

    # 分别获取最后和最前块的块号
    last_block = Block(query_last_block(mydb)).get_number()
    head_number = Block(query_first_block(mydb)).get_number()

    # 循环获取块信息，并解析
    while True:
        # 如果网速非常快，或者用的本地节点，或许可以加个 sleep(1)减少浪费资源?

        # 如果是块没更新，就再获取，总之不能漏
        new_block = api.get_block(last_block + 1)
        if new_block == {}:
            continue

        # 始终保持最后一块和最前一块差1天时间，检查最前面的一块是不是过期了，是就减去
        if cut_head(head_number):
            head_number += 1
            continue

        analyze(Block(new_block))
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
# 存在数据库里的 地址 都是hex形式的，因为API也是这个形式，方便程序处理
# 地址在查询的时候会实时base58处理，方便查看
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
            5.query VoteWitnessContract
            6.query FreezeBalanceContract transactions (if frozen_duration and frozen_balance are both 0 means UnfreezeBalanceContract)
            7.query transactions of other type
            '''
        )
        if chose == '1':
            tmp = query_big_transfer(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'owner_address', 'to_address', 'amount', 'others']
            for i in tmp:
                i[1] = hex_to_base58(i[1]).decode()  # 地址类型都要做这个处理
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
                if i[3]:
                    i[3] = hex_to_base58(i[3]).decode()
                tb.add_row(i)
            print(tb)

        elif chose == '3':
            tmp = query_top_app(mydb)
            # 获取balance,并求和
            for one_app in tmp:
                addr_list = one_app[0]
                for addr_single in addr_list:
                    one_app[4] += api.get_balance(addr_single)
            tb = pt.PrettyTable()
            tb.field_names = ['addresses', 'name', 'all_transaction_count', 'day_transaction', 'balance',
                              'day_transfer', 'DAU']
            for i in tmp:
                i[0] = 'too long'
                i[6] = len(i[6])
                tb.add_row(i)
            print(tb)

        # 因为有时候屏幕一行显示不下，所以去掉了'to_address'这个字段
        elif chose == '4':
            tmp = query_big_token_transfer(mydb, 0)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'asset_name', 'owner_address', 'amount', 'others']
            for i in tmp:
                i[2] = hex_to_base58(i[2]).decode()
                i[1] = bytes.fromhex(i[1]).decode() if i[1] != "5f" else "trade TRX for another token"
                tb.add_row(i)
            print(tb)
        elif chose == '5':
            tmp = query_vote(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'owner_address', 'data']
            for i in tmp:
                i[1] = hex_to_base58(i[1]).decode()  # 地址类型都要做这个处理
                # 以后再想办法
                i[2] = 'too long, please get information from database'
                tb.add_row(i)
            print(tb)
        elif chose == '6':
            tmp = query_freeze(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'owner_address', 'frozen_balance', 'frozen_duration']
            for i in tmp:
                i[1] = hex_to_base58(i[1]).decode()  # 地址类型都要做这个处理
                if i[2] == 0 and i[3] == 0:
                    i[3] = 'UnfreezeBalanceContract'
                tb.add_row(i)
            print(tb)

        elif chose == '7':
            tmp = query_other(mydb)
            tb = pt.PrettyTable()
            tb.field_names = ['txID', 'type', 'owner_address', 'data']
            for i in tmp:
                i[2] = hex_to_base58(i[2]).decode()  # 地址类型都要做这个处理
                # 以后再想办法
                i += ['too long, please get information from database']
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
