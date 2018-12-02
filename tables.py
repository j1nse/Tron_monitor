_tables = dict()
_tables['block'] = ''' \
CREATE TABLE `block` ( \
`blockID` char(64) PRIMARY KEY NOT NULL, \
`block_header` varchar(1024) NOT NULL, \
`transactions` varchar(6400) NOT NULL \
) \
'''

_tables['transactions'] = ''' \
CREATE TABLE `transactions`( \
`txID` char(64) PRIMARY KEY NOT NULL, \
`ret` varchar(25), \
`signature` char(130)  NOT NULL, \
`raw_data` varchar(1024) NOT NULL \
) \
'''

_tables['raw_data'] = ''' \
CREATE TABLE `raw_data`( \
`txID` char(64) PRIMARY KEY NOT NULL, \
`contract` varchar(1024), \
`fee_limit` varchar(25), \
`timestamp` varchar(25) \
) \
'''

_tables['top_DAPP'] = ''' \
CREATE TABLE `top_DAPP` ( \
address char(42) PRIMARY KEY NOT NULL, \
all_transaction_count  BIGINT NOT NULL, \
day_transaction BIGINT NOT NULL, \
balance BIGINT NOT NULL \
) \
'''

_tables['big_transfer'] = ''' \
CREATE TABLE `big_transfer`( \
`txID` char(64) PRIMARY KEY NOT NULL, \
owner_address char(42), \
to_address  char(42), \
amount FLOAT, \
others varchar(1024) \
) \
'''

_tables['big_token_transfer'] = ''' \
CREATE TABLE `big_token_transfer`( \
`txID` char(64) PRIMARY KEY NOT NULL , \
asset_name varchar(25) ,\
owner_address char(42), \
to_address char(42), \
amount FLOAT, \
others varchar(1024) \
) \
'''
