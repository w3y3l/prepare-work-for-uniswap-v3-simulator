from web3 import Web3

# 连接到以太坊网络
node_url = 'http://127.0.0.1:2024'
web3 = Web3(Web3.HTTPProvider(node_url))

# 确保连接
if not web3.is_connected():
    print("无法连接到以太坊节点")
    exit(1)

# 您的账户信息
private_key = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'  # 替换为您的私钥
my_account = web3.eth.account.from_key(private_key)

# WETH 合约地址和标准 ERC-20 ABI
weth_contract_address = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'  # 替换为 WETH 合约地址
erc20_abi = """[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]"""

# 创建 WETH 合约实例
weth_contract = web3.eth.contract(address=weth_contract_address, abi=erc20_abi)

# Uniswap 合约地址
uniswap_address = Web3.to_checksum_address("0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640") # 替换为 Uniswap 合约地址


# 设置授权数量，例如授权 10 WETH
amount_to_approve = web3.to_wei(20, 'ether')  # 可根据需要调整数值

# 构建授权交易
approve_tx = weth_contract.functions.approve(
    uniswap_address, 
    amount_to_approve
).build_transaction({
    'from': my_account.address,
    'nonce': web3.eth.get_transaction_count(my_account.address),
    'gas': 200000,
    'gasPrice': web3.to_wei('50', 'gwei')
})

# 签名交易
signed_approve_tx = my_account.sign_transaction(approve_tx)

# 发送交易
approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
print(f"授权交易已发送，交易哈希：{approve_tx_hash.hex()}")

# 等待交易确认
approve_tx_receipt = web3.eth.wait_for_transaction_receipt(approve_tx_hash)
print(f"授权交易已确认，区块号：{approve_tx_receipt.blockNumber}")



# 检查授权
allowance = weth_contract.functions.allowance(my_account.address, uniswap_address).call()
print(f"已授权给 Uniswap 的代币数量: {web3.from_wei(allowance, 'ether')} Tokens")
