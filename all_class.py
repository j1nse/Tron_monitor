class Transactions:
    txID = ''
    ret = []
    signature = []
    raw_data = {}
    txdata = {}
    type = ''

    def __init__(self, txID, ret, signature, raw_data):
        self.txID = txID
        self.ret = ret
        self.signature = signature
        self.raw_data = raw_data
        self.txdata = raw_data['contract'][0]['parameter']['value']
        self.type = raw_data['contract'][0]['type']

    def get_txID(self):
        return self.txID

    def get_ret(self):
        return self.ret

    def get_signature(self):
        return self.signature

    def get_raw_data(self):
        return self.raw_data

    def get_txdata(self):
        return self.txdata

    def get_type(self):
        return self.type

    def get_data(self):
        return self.txdata['data']

    def get_owner(self):
        return self.txdata['owner_address']

    def get_contract(self):
        return self.raw_data['contract']

    def get_amount(self):
        return self.txdata['amount']

    def get_to_address(self):
        return self.txdata['to_address']

    def get_contract_address(self):
        return self.txdata['contract_address']

    def get_call_value(self):
        if self.txdata['call_value']:
            return self.txdata['call_value']
        else:
            return ''

    def get_status(self):
        return self.ret[0]['contractRet']

    def get_timestamp(self):
        return self.raw_data['timestamp']

    def get_asset_name(self):
        return self.txdata['asset_name']


class Top:
    address = ''
    all_transaction_count = 0
    day_transaction = 0
    balance_count = 0

    def __init__(self, address, all_transaction_count=0, day_transaction=0, balance_count=0):
        self.address = address
        self.all_transaction_count = all_transaction_count
        self.day_transaction = day_transaction
        self.balance_count = balance_count

    def get_address(self):
        return self.address

    def get_all_transaction_count(self):
        return self.all_transaction_count

    def get_day_transaction(self):
        return self.all_transaction_count

    def get_balance_count(self):
        return self.balance_count


class Block:
    blockID = ''
    block_header = {}
    transactions = {}

    def __init__(self, ori):
        self.blockID = ori['blockID']
        self.block_header = ori['block_header']
        for i in ori['transactions']:
            self.transactions[i['txID']] = i['raw_data']['contract'][0]['type']

    def get_transactions(self):
        return self.transactions

    def get_blockID(self):
        return self.blockID

    def get_header(self):
        return self.block_header

    def get_number(self):
        return self.block_header['raw_data']['number']

    def get_txTrieRoot(self):
        return self.block_header['raw_data']['txTrieRoot']

    def get_witness_address(self):
        return self.block_header['raw_data']['witness_address']

    def get_parentHash(self):
        return self.block_header['raw_data']['parentHash']

    def get_version(self):
        return self.block_header['raw_data']['version']

    def get_timestamp(self):
        return self.block_header['raw_data']['timestamp']

    def get_witness_signature(self):
        return self.block_header['witness_signature']
