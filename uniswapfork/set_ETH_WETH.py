from web3 import Web3

node_url = 'http://127.0.0.1:2024'
web3 = Web3(Web3.HTTPProvider(node_url))

# 确保连接
if not web3.is_connected():
    print("无法连接到节点")
    exit(1)


# 您的账户信息
# 设置您的账户
my_account = web3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')

# WETH 合约信息
weth_contract_address= Web3.to_checksum_address('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')

weth_contract_abi = '[{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}, {"constant":true,"inputs":[],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

# 创建 WETH 合约实例
weth_contract = web3.eth.contract(address=weth_contract_address, abi=weth_contract_abi)

# 设置要转换的 ETH 数量
amount_eth_to_wrap = web3.to_wei(10, 'ether')  # 例如，包装 1 ETH

# 构建交易
wrap_tx = weth_contract.functions.deposit().build_transaction({
    'from': my_account.address,
    'value': amount_eth_to_wrap,
    'gas': 200000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': web3.eth.get_transaction_count(my_account.address)
})

# 签名交易
signed_tx = my_account.sign_transaction(wrap_tx)

# 发送交易
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

