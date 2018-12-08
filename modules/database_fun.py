from json import dumps, loads
from modules.all_class import *


# 这个文件里包含所有针对数据库的函数，根据名字就知道作用了

# 反序列化str对象
def deserialization(tmp, all_data):
    for i in tmp:
        one_row = []
        for j in i:
            if type(j) == str:
                one_row.append(loads(j))
            else:
                one_row.append(j)
        all_data.append(one_row)
    return all_data


def insert_block(db, block):
    cursor = db.cursor()
    word = ''' \
INSERT INTO block \
( blockID,number, block_header, transactions ) \
VALUES ('{}',{},'{}','{}') \
'''.format(
        dumps(block.get_blockID()).replace('\"', '\\"'),
        block.get_number(),
        dumps(block.get_header()).replace('\"', '\\"'),
        dumps({}).replace('\"', '\\"')
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_transaction(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO transactions \
( txID, ret, signature, raw_data ) \
VALUES ('{}','{}','{}','{}') \
'''.format(
        dumps(transaction.get_txID()).replace('\"', '\\"'),
        dumps(transaction.get_ret()).replace('\"', '\\"'),
        dumps(transaction.get_signature()).replace('\"', '\\"'),
        dumps(transaction.get_raw_data()).replace('\"', '\\"')
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


"""
def insert_raw_data(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO raw_data \
( txID, contract, fee_limit, timestamp ) \
VALUES ({},{},{},{}) \
'''.format(
        dumps(transaction.get_txID()),
        dumps(transaction.get_contract()),
        dumps(transaction.get_fee_limit()),
        dumps(transaction.get_timestamp())
    )
    cursor.execute(word)
    db.commit()
    cursor.close()
"""


def insert_top_dapp(db, top):
    cursor = db.cursor()
    word = '''\
INSERT INTO top_DAPP \
( addresses,name, all_transaction_count, day_transaction, balance, day_transfer,users ) \
VALUES ('{}','{}',{},{},{},{},'{}')\
'''.format(
        dumps(top.get_addresses()).replace('\"', '\\"'),
        dumps(top.get_name()).replace('\"', '\\"'),
        dumps(top.get_all_transaction_count()),
        dumps(top.get_day_transaction()),
        dumps(top.get_balance()),
        dumps(top.get_day_transfer()),
        dumps(top.get_users()).replace('\"', '\\"')
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_big_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO big_transfer \
( txID,owner_address, to_address, amount ) \
VALUES ('{}','{}','{}',{}) \
'''.format(
        dumps(transaction.get_txID()).replace('\"', '\\"'),
        dumps(transaction.get_owner_address()).replace('\"', '\\"'),
        dumps(transaction.get_to_address()).replace('\"', '\\"'),
        transaction.get_amount()
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def query_last_block(db):
    cursor = db.cursor()
    word = '''\
SELECT blockID,number,block_header \
 FROM block ORDER BY number DESC LIMIT 1 \
 '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []
    if tmp:
        all_data = deserialization(tmp, all_data)
    else:
        return {}

    # 只返回需要的信息即可
    result = {"blockID": all_data[0][0],
              "block_header": all_data[0][2],
              'transactions': {}
              }
    cursor.close()
    return result


def query_first_block(db):
    cursor = db.cursor()
    word = '''\
SELECT blockID,number, block_header \
 FROM block ORDER BY number ASC LIMIT 1 \
 '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []
    # 如果不为空，就反序列化，否则直接返回空字典
    if tmp:
        all_data = deserialization(tmp, all_data)
    else:
        return {}

    # 只返回需要的信息即可
    result = {"blockID": all_data[0][0],
              "block_header": all_data[0][2],
              'transactions': {}
              }
    cursor.close()
    return result


def insert_big_token_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO big_token_transfer \
( txID,asset_name,owner_address, to_address, amount ) \
VALUES ('{}','{}','{}','{}',{}) \
'''.format(
        dumps(transaction.get_txID()).replace('\"', '\\"'),
        dumps(transaction.get_asset_name()).replace('\"', '\\"'),
        dumps(transaction.get_owner_address()).replace('\"', '\\"'),
        dumps(transaction.get_to_address()).replace('\"', '\\"'),
        transaction.get_amount()
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def query_big_transfer(db):
    cursor = db.cursor()
    word = '''\
    SELECT txID,owner_address,to_address,amount,others \
    FROM big_transfer ORDER BY amount DESC \
    '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []
    # 这个循环用于把str类型的变量都反序列化
    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data


def query_big_token_transfer(db, chose):
    cursor = db.cursor()
    if chose == 1:
        word = '''\
SELECT txID,asset_name,owner_address,to_address,amount,others \
FROM big_token_transfer ORDER BY amount DESC \
 '''
    elif chose == 0:
        word = '''\
SELECT txID,asset_name,owner_address,amount,others \
 FROM big_token_transfer ORDER BY amount DESC \
'''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []
    # 这个循环用于把str类型的变量都反序列化
    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data


def query_top_app(db) -> list:
    cursor = db.cursor()
    word = '''\
    SELECT addresses,name,all_transaction_count,day_transaction,balance,day_transfer,users \
    FROM top_DAPP ORDER BY all_transaction_count DESC \
    '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []
    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data


def update_top_app(db, name, all_transaction_count, day_transaction, balance, day_transfer, users):
    cursor = db.cursor()
    word = '''\
    UPDATE top_DAPP SET all_transaction_count = {},day_transaction={},balance={},day_transfer={},users='{}' WHERE name = '{}' \
    '''.format(
        all_transaction_count, day_transaction, balance, day_transfer, dumps(users).replace('\"', '\\"'),
        "\"" + name + "\""
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def clear_block(db):
    cursor = db.cursor()
    word = '''\
        TRUNCATE TABLE `block` \
        '''
    cursor.execute(word)
    db.commit()
    cursor.close()


def clear_trans(db):
    cursor = db.cursor()
    word = '''\
            TRUNCATE TABLE `transactions` \
            '''
    cursor.execute(word)
    db.commit()
    cursor.close()


def clear_top_DAPP(db):
    cursor = db.cursor()
    word = '''\
TRUNCATE TABLE `top_DAPP`; \
'''
    cursor.execute(word)
    db.commit()
    cursor.close()


def clear_top_big_transfer(db):
    cursor = db.cursor()
    word = '''\
TRUNCATE TABLE `big_transfer` \
'''
    cursor.execute(word)
    db.commit()
    cursor.close()


def clear_top_big_token_transfer(db):
    cursor = db.cursor()
    word = '''\
TRUNCATE TABLE `big_token_transfer` \
'''
    cursor.execute(word)
    db.commit()
    cursor.close()


def delete_block(db, number):
    cursor = db.cursor()
    word = '''\
DELETE FROM `block` where number = {}  \
'''.format(number)
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_other(db, tx: Transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO other_type \
( txID,type,owner_address, data ) \
VALUES ('{}','{}','{}','{}') \
 '''.format(
        dumps(tx.get_txID()).replace('\"', '\\"'),
        dumps(tx.get_type()).replace('\"', '\\"'),
        dumps(tx.get_owner_address()).replace('\"', '\\"'),
        dumps(tx.get_txdata()).replace('\"', '\\"')

    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def query_other(db):
    cursor = db.cursor()
    word = '''\
SELECT txID,type,owner_address \
FROM other_type ORDER BY type\
'''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []

    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data


def insert_freeze(db, tx: Transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO freeze_balance_contract \
( txID,owner_address, frozen_balance,frozen_duration ) \
VALUES ('{}','{}',{},{}) \
'''.format(
        dumps(tx.get_txID()).replace('\"', '\\"'),
        dumps(tx.get_owner_address()).replace('\"', '\\"'),
        dumps(tx.get_frozen_balance()).replace('\"', '\\"'),
        dumps(tx.get_frozen_duration()).replace('\"', '\\"'),

    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_vote(db, tx: Transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO vote_witness_contract \
( txID,owner_address, votes ) \
VALUES ('{}','{}','{}') \
'''.format(
        dumps(tx.get_txID()).replace('\"', '\\"'),
        dumps(tx.get_owner_address()).replace('\"', '\\"'),
        dumps(tx.get_txdata()).replace('\"', '\\"')

    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def query_vote(db):
    cursor = db.cursor()
    word = '''\
SELECT txID,owner_address,votes \
FROM vote_witness_contract ORDER BY owner_address\
'''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []

    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data


def query_freeze(db):
    cursor = db.cursor()
    word = '''\
SELECT txID,owner_address,frozen_balance,frozen_duration \
FROM freeze_balance_contract ORDER BY frozen_duration\
    '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    all_data = []

    if tmp:
        all_data = deserialization(tmp, all_data)
    cursor.close()
    return all_data
