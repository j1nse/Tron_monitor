from json import loads, dumps


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


def insert_big_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO raw_data \
( owner_address, to_address, amount ) \
VALUES ({},{},{}) \	
'''.format(
        dumps(transaction.get_owner()),
        dumps(transaction.get_get_to_address()),
        dumps(transaction.get_amount()),
    )
    cursor.execute(word)
    db.commit()


def insert_big_token_transfer(db, transaction):
    cursor = db.cursor()
    word = '''\
INSERT INTO raw_data \
( owner_address, to_address, amount ) \
VALUES ({},{},{}) \	
'''.format(
        dumps(transaction.get_asset_name()),
        dumps(transaction.get_owner_address()),
        dumps(transaction.get_to_address()),
        dumps(transaction.get_amount())
    )
    cursor.execute(word)
    db.commit()
