from web3 import Web3

RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/uCcmczhSkVZjQFZ4btat1"

w3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_tx(tx_hash):
    return w3.eth.get_transaction(tx_hash)

def get_receipt(tx_hash):
    return w3.eth.get_transaction_receipt(tx_hash)