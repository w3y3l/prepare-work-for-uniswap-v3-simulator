const { Web3 } = require('web3');

async function checkGasPrice() {
  // 连接到以太坊节点
  const web3 = new Web3('http://127.0.0.1:2024');

  try {
    // 获取当前 gas 价格
    const gasPrice = await web3.eth.getGasPrice();
    console.log('Current Gas Price:', gasPrice);

    // 获取当前区块的 gas 限制
    const block = await web3.eth.getBlock('latest');
    console.log('Current block gas limit:', block.gasLimit);

    // 计算交易费用
    const gasLimit = '1000000'; // 示例中的 gas 限制
    const gasFeeInWei = BigInt(gasLimit) * BigInt(gasPrice);
    const gasFeeInEth = web3.utils.fromWei(gasFeeInWei.toString(), 'ether');
    console.log('Transaction Fee in ETH:', gasFeeInEth);
  } catch (error) {
    console.error('Error fetching gas data:', error);
  }
}

// 调用 async 函数
checkGasPrice();
