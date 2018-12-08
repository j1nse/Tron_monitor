# 这个文件包含所有数据库的表的设计

_tables = dict()
_tables['block'] = ''' \
CREATE TABLE `block` ( \
`blockID` char(66) PRIMARY KEY NOT NULL, \
`number` BIGINT  NOT NULL, \
`block_header` varchar(1024) NOT NULL, \
`transactions` varchar(8000) NOT NULL \
) \
'''

_tables['transactions'] = ''' \
CREATE TABLE `transactions`( \
`txID` char(66) PRIMARY KEY NOT NULL, \
`ret` varchar(30), \
`signature` char(138)  NOT NULL, \
`raw_data` varchar(1024) NOT NULL \
) \
'''

_tables['top_DAPP'] = ''' \
CREATE TABLE `top_DAPP` ( \
addresses varchar(500) NOT NULL, \
name varchar(30) PRIMARY KEY NOT NULL,
all_transaction_count  BIGINT NOT NULL, \
day_transaction BIGINT NOT NULL, \
balance BIGINT NOT NULL, \
day_transfer FLOAT NOT NULL, \
users varchar(50000) \
) \
'''

_tables['big_transfer'] = ''' \
CREATE TABLE `big_transfer`( \
`txID` char(66) PRIMARY KEY NOT NULL, \
owner_address char(44), \
to_address  char(44), \
amount FLOAT, \
others varchar(1024) \
) \
'''

_tables['big_token_transfer'] = ''' \
CREATE TABLE `big_token_transfer`( \
`txID` char(66) PRIMARY KEY NOT NULL , \
asset_name varchar(70) ,\
owner_address char(44), \
to_address char(44), \
amount FLOAT, \
others varchar(1024) \
) \
'''

_tables['other_type'] = ''' \
CREATE TABLE `other_type`( \
`txID` char(66) PRIMARY KEY NOT NULL , \
`type` varchar(50) NOT NULL, \
owner_address char(44), \
data varchar(10000) \
) \
'''
# VoteWitnessContract
_tables['vote_witness_contract'] = ''' \
CREATE TABLE `vote_witness_contract`( \
`txID` char(66) PRIMARY KEY NOT NULL , \
owner_address char(44), \
votes varchar(10000) \
) \
'''

_tables['freeze_balance_contract'] = ''' \
CREATE TABLE `freeze_balance_contract`( \
`txID` char(66) PRIMARY KEY NOT NULL , \
owner_address char(44), \
frozen_balance FLOAT, \
frozen_duration INT \
) \
'''

# 創建時間，bytecode各種信息

_tables['dapp_info'] = ''' \
CREATE TABLE `dapp_info`( \
`name` varchar(70) PRIMARY KEY NOT NULL , \
create_time BIGINT ,\
bytecode varchar(2048) \
) \
'''
