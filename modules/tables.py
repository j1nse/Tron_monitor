# 这个文件包含所有数据库的表的设计

_tables = dict()
_tables['block'] = ''' \
CREATE TABLE `block` ( \
`blockID` varchar(70) PRIMARY KEY NOT NULL, \
`number` BIGINT  NOT NULL, \
`block_header` varchar(1024) NOT NULL, \
`transactions` varchar(8000) NOT NULL \
) \
'''

_tables['transactions'] = ''' \
CREATE TABLE `transactions`( \
`txID` varchar(70) PRIMARY KEY NOT NULL, \
`ret` varchar(30), \
`signature` varchar(140)  NOT NULL, \
`raw_data` varchar(1024) NOT NULL \
) \
'''
# 废弃
"""
_tables['raw_data'] = ''' \
CREATE TABLE `raw_data`( \
`txID` varchar(70) PRIMARY KEY NOT NULL, \
`contract` varchar(1024), \
`fee_limit` varchar(30), \
`timestamp` varchar(30) \
) \
'''
"""

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
`txID` varchar(70) PRIMARY KEY NOT NULL, \
owner_address varchar(50), \
to_address  varchar(50), \
amount FLOAT, \
others varchar(1024) \
) \
'''

_tables['big_token_transfer'] = ''' \
CREATE TABLE `big_token_transfer`( \
`txID` varchar(70) PRIMARY KEY NOT NULL , \
asset_name varchar(70) ,\
owner_address varchar(50), \
to_address varchar(50), \
amount FLOAT, \
others varchar(1024) \
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
