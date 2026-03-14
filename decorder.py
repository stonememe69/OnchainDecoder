from web3 import Web3

TRANSFER_SIG = Web3.keccak(text="Transfer(address,address,uint256)").hex()

TOKEN_CACHE = {}

def decode_transfers(receipt, w3):

    transfers = []

    for log in receipt["logs"]:

        if log["topics"][0].hex() == TRANSFER_SIG:

            from_addr = "0x" + log["topics"][1].hex()[-40:]
            to_addr = "0x" + log["topics"][2].hex()[-40:]

            raw_amount = int.from_bytes(log["data"], "big")

            token = log["address"]

            symbol, decimals = get_token_info(w3, token)

            amount = raw_amount / (10 ** decimals)

            transfers.append({
                "from": from_addr,
                "to": to_addr,
                "amount": amount,
                "symbol": symbol,
                "token": token
            })

    return transfers
    
ERC20_ABI = [
 {
  "constant":True,
  "inputs":[],
  "name":"symbol",
  "outputs":[{"name":"","type":"string"}],
  "type":"function"
 },
 {
  "constant":True,
  "inputs":[],
  "name":"decimals",
  "outputs":[{"name":"","type":"uint8"}],
  "type":"function"
 }
]

def get_token_info(w3, address):

    if address in TOKEN_CACHE:
        return TOKEN_CACHE[address]

    contract = w3.eth.contract(address=address, abi=ERC20_ABI)

    symbol = contract.functions.symbol().call()
    decimals = contract.functions.decimals().call()

    TOKEN_CACHE[address] = (symbol, decimals)

    return symbol, decimals