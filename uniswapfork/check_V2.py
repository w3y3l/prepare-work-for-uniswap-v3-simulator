from web3 import Web3
import json
# 初始化 Web3
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:2024'))  # 替换为您的节点地址

# 您的账户地址
my_account_address = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
my_account = web3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')

# 检查 ETH 余额
eth_balance = web3.eth.get_balance(my_account_address)
print(f"ETH 余额: {web3.from_wei(eth_balance, 'ether')} ETH")

# WETH 合约地址和 ABI
weth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
with open('weth.json', 'r') as file:
    weth_contract_abi = json.load(file)


# 创建 WETH 合约实例
weth_contract = web3.eth.contract(address=weth_contract_address, abi=weth_contract_abi)

# 将 ETH 包装成 WETH
eth_to_convert = web3.to_wei(1, 'ether')  # 转换 1 ETH
wrap_tx = weth_contract.functions.deposit().build_transaction({
    'from': my_account_address,
    'value': eth_to_convert,
    'gas': 200000,
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(my_account_address),
})

signed_wrap_tx = my_account.sign_transaction(wrap_tx)
web3.eth.send_raw_transaction(signed_wrap_tx.rawTransaction)

# 授权 Uniswap V2 使用 WETH
uniswap_v2_router_address = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
approve_tx = weth_contract.functions.approve(
    uniswap_v2_router_address,
    eth_to_convert
).build_transaction({
    'from': my_account_address,
    'gas': 200000,
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(my_account_address) + 1,
})

signed_approve_tx = my_account.sign_transaction(approve_tx)
web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)

# 检查 Uniswap V2 合约被授权花费的 WETH 数量
allowance = weth_contract.functions.allowance(my_account_address, uniswap_v2_router_address).call()
print(f"授权给 Uniswap V2 的 WETH 数量: {web3.from_wei(allowance, 'ether')} WETH")
