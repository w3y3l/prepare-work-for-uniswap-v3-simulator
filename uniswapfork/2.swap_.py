#以weth/usdc为例，进行一笔swap尝试
#输出swap前后账户信息

from web3 import Web3
import time

def print_account_info(web3, account_address, token_contract=None, weth_contract=None):
    eth_balance = web3.eth.get_balance(account_address)
    print(f"账户地址: {account_address}")
    print(f"ETH 余额: {web3.from_wei(eth_balance, 'ether')} ETH")

    if token_contract is not None:
        token_balance = token_contract.functions.balanceOf(account_address).call()
        print(f"USDC余额: {web3.from_wei(token_balance, 'ether')} Tokens")

    if weth_contract is not None:
        weth_balance = weth_contract.functions.balanceOf(account_address).call()
        print(f"WETH 余额: {web3.from_wei(weth_balance, 'ether')} WETH")



node_url = 'http://127.0.0.1:2024'
web3 = Web3(Web3.HTTPProvider(node_url))
w = web3.eth.get_transaction("0x813749034340f6e300b45afff793e02d5378f5d0264b963c0888fd95c7105f05")
print(w)
# 确保连接
if not web3.is_connected():
    print("无法连接到节点")
    exit(1)

# 设置您的账户
    
my_account = web3.eth.account.from_key('0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')
uniswap_abi ="""[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH9","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH9","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactInputParams","name":"params","type":"tuple"}],"name":"exactInput","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bytes","name":"path","type":"bytes"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"}],"internalType":"struct ISwapRouter.ExactOutputParams","name":"params","type":"tuple"}],"name":"exactOutput","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMaximum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactOutputSingleParams","name":"params","type":"tuple"}],"name":"exactOutputSingle","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes[]","name":"data","type":"bytes[]"}],"name":"multicall","outputs":[{"internalType":"bytes[]","name":"results","type":"bytes[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"refundETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowed","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitAllowedIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"selfPermitIfNecessary","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"sweepToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"sweepTokenWithFee","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"}],"name":"unwrapWETH9","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountMinimum","type":"uint256"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"feeBips","type":"uint256"},{"internalType":"address","name":"feeRecipient","type":"address"}],"name":"unwrapWETH9WithFee","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]"""
# uniswap_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
#router contract
uniswap_address = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
checksum_address = Web3.to_checksum_address(uniswap_address)
uniswap_contract = web3.eth.contract(address=checksum_address, abi=uniswap_abi)
#usdc
TOKEN_ADDRESS = Web3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")
TOKEN_ABI = """[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"}]"""

weth_contract_address=Web3.to_checksum_address("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
# 如果需要查看特定代币的余额，创建代币合约实例
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=TOKEN_ABI)  # 替换为代币地址和ABI
weth_contract = web3.eth.contract(address=weth_contract_address,abi=TOKEN_ABI )
# 打印 swap 交易前的账户信息


print("Swap 交易前的账户信息:")
print_account_info(web3, my_account.address, token_contract, weth_contract)

# 获取交易前的 WETH 和 USDC 余额
weth_balance_before = weth_contract.functions.balanceOf(my_account.address).call()
usdc_balance_before = token_contract.functions.balanceOf(my_account.address).call()


# 设置 Uniswap 交易参数
recipient = Web3.to_checksum_address("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266") # 收币地址
amount_in = web3.to_wei(0.01, 'ether')  # 交换 1 WETH，数量根据您的情况调整
amount_out_min = 1624 # 最小接收的 USDC 数量，这里设置为 0 表示接受任何数量的 USDC
fee = 10000
token_out = weth_contract_address  # WETH 合约地址
token_in = TOKEN_ADDRESS  # USDC 合约地址
deadline = int(time.time()) + 600  # 设置交易截止时间，例如 10 分钟后

# 构建交易
tx = uniswap_contract.functions.exactInputSingle(
    (weth_contract_address,
    TOKEN_ADDRESS,
    fee,
    recipient,
    deadline,
    amount_in,  # 注意，这里是负数，表示卖出
    amount_out_min,
    0)
).build_transaction({
    'from': my_account.address,
    'gas': 2000000,
    'gasPrice': web3.to_wei('50', 'gwei'),
    'nonce': web3.eth.get_transaction_count(my_account.address),
    'value': 0  # 由于是 ERC-20 交换，所以 value 为 0
})
# 签名交易
signed_tx = my_account.sign_transaction(tx)

# 发送交易
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f"交易已发送，交易哈希：{tx_hash.hex()}")

# 等待交易确认
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"交易已确认，区块号：{tx_receipt.blockNumber}")


# 打印 swap 交易后的账户信息
# print("\nSwap 交易后的账户信息:")
# print_account_info(web3, my_account.address, token_contract, weth_contract)
# 获取交易后的 WETH 和 USDC 余额
weth_balance_after = weth_contract.functions.balanceOf(my_account.address).call()
usdc_balance_after = token_contract.functions.balanceOf(my_account.address).call()

# 计算变化量
weth_change = weth_balance_before - weth_balance_after
usdc_change = usdc_balance_after - usdc_balance_before

# 打印交易后的账户信息和交易结果
print("\nSwap 交易后的账户信息:")
print_account_info(web3, my_account.address, token_contract, weth_contract)

# 打印交易的结果
print(f"\n交换的 WETH 数量: {web3.from_wei(weth_change, 'ether')} WETH")
print(f"获得的 USDC 数量: {web3.from_wei(usdc_change, 'ether')} USDC")

# 计算并打印比例
if weth_change > 0:
    rate = usdc_change / weth_change
    print(f"兑换比例：1 WETH = {rate} USDC")
else:
    print("未发生有效的兑换")