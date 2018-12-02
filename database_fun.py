from json import loads, dumps
# 这个文件里包含所有针对数据库的函数，根据名字就知道作用了

def insert_block(db, block):
    cursor = db.cursor()
    word = ''' \
INSERT INTO block \
( blockID, block_header, transactions ) \
VALUES ({},{},{}) \
'''.format(
        dumps(block.get_blockID()),
        dumps(block.get_header()),
        dumps(block.get_transactions())
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_transaction(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO transactions \
( txID, ret, signature, raw_data ) \
VALUES ({},{},{},{}) \	
'''.format(
        dumps(transaction.get_txID()),
        dumps(transaction.get_ret()),
        dumps(transaction.get_signature()),
        dumps(transaction.get_raw_data())
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


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


def insert_top_DAPP(db, top):
    cursor = db.cursor()
    word = '''\
INSERT INTO top_DAPP \
( address, all_transaction_count, day_transaction, balance_count ) \
VALUES ({},{},{},{}) \	
'''.format(
        dumps(top.get_address()),
        dumps(top.get_all_transaction_count()),
        dumps(top.get_day_transaction()),
        dumps(top.get_balance_count())
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_big_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO big_transfer \
( txID,owner_address, to_address, amount ) \
VALUES ({},{},{},{}) \	
'''.format(
        dumps(transaction.get_txID()),
        dumps(transaction.get_owner()),
        dumps(transaction.get_get_to_address()),
        dumps(transaction.get_amount()),
    )
    cursor.execute(word)
    db.commit()
    cursor.close()


def insert_big_token_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO big_token_transfer \
( txID,asset_name,owner_address, to_address, amount ) \
VALUES ({},{},{},{},{}) \	
'''.format(
        dumps(transaction.get_txID()),
        dumps(transaction.get_asset_name()),
        dumps(transaction.get_owner_address()),
        dumps(transaction.get_to_address()),
        dumps(transaction.get_amount())
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
    cursor.close()
    return tmp


def query_big_token_transfer(db):
    cursor = db.cursor()
    word = '''\
    SELECT txID,asset_name,owner_address,to_address,amount,others \
    FROM big_token_transfer ORDER BY amount DESC \
    '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    cursor.close()
    return tmp


def query_top_app(db):
    cursor = db.cursor()
    word = '''\
    SELECT address,all_transaction_count,day_transaction,balance \
    FROM top_DAPP ORDER BY all_transaction_count DESC \
    '''
    cursor.execute(word)
    tmp = cursor.fetchall()
    cursor.close()
    return tmp


def update_top_app(db, address, all_transaction_count, day_transaction, balance):
    cursor = db.cursor()
    word = '''\
    UPDATE top_DAPP SET all_transaction_count = {},day_transaction={},balance={} WHERE address = '{}' \
    '''.format(
        address, all_transaction_count, day_transaction, balance
    )
    cursor.execute(word)
    db.commit()
    cursor.close()

