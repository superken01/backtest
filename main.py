from web3 import Web3

url = "https://api.avax.network/ext/bc/C/rpc"
w3 = Web3(Web3.HTTPProvider(url))
print(w3.isConnected())

qi_token_address = Web3.toChecksumAddress(
    "0xd8fcda6ec4bdc547c0827b8804e89acd817d56ef")

block_filter = w3.eth.filter({
    'fromBlock':
    18941584,
    'toBlock':
    18942382,
    'address':
    qi_token_address,
    "topics":
    ['0x4dec04e750ca11537cabcd8a9eab06494de08da3735bc8871cd41250e190bc04']
})

# for e in block_filter.get_all_entries():
#     print(e)
# abi = '''
# contract IQiToken {
#     function mint(uint256 amount) external returns (uint256);
# }
# '''
abi = [{
    "constant": True,
    "inputs": [],
    "name": "supplyRatePerTimestamp",
    "outputs": [{
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
    }],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": True,
    "inputs": [],
    "name": "borrowRatePerTimestamp",
    "outputs": [{
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
    }],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}]
qi_token_contract = w3.eth.contract(qi_token_address, abi=abi)
print(qi_token_contract.address)
supply_apr = qi_token_contract.functions.supplyRatePerTimestamp().call(
) * 365 * 24 * 60 * 60 / 10**18
borrow_apr = qi_token_contract.functions.borrowRatePerTimestamp().call(
) * 365 * 24 * 60 * 60 / 10**18

supply_apy = (1 + supply_apr / 365)**365 - 1
borrow_apy = (1 + borrow_apr / 365)**365 - 1
print(supply_apy, borrow_apy)

# import time

# block_number = w3.eth.block_number
# while True:
#     # print(block_number, block_number - 5000)
#     block_filter = w3.eth.filter({
#         'fromBlock': block_number - 5000,
#         'toBlock': block_number,
#         'address': address,
#         "topics": ['0xf279e6a1f5e320cca91135676d9cb6e44ca8a08c0b88342bcdb1144f6511b568']
#     })
#     for e in block_filter.get_all_entries():
#         print(block_number, block_number - 5000, e.transactionHash.hex(), ':', int(e.data, 16) / 10e18)
#         # w3.eth.get_block(e.blockNumber).timestamp
#     block_number -= 5001
#     time.sleep(0.1)