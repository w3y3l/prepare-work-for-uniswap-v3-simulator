const { Web3 } = require('web3');
const web3 = new Web3('http://127.0.0.1:2024');

async function checkBalanceAndGas() {
  const senderAddress = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
  const gasLimit = '13599248078';
  const gasPrice = '300000000000';

  try {
    const balance = await web3.eth.getBalance(senderAddress);
    const balanceInEth = web3.utils.fromWei(balance, 'ether');

    console.log('Balance of', senderAddress, 'is', balanceInEth, 'ETH');

    const gasFeeInWei = BigInt(gasLimit) * BigInt(gasPrice);
    const gasFeeInEth = web3.utils.fromWei(gasFeeInWei.toString(), 'ether');

    console.log('Transaction Fee in ETH:', gasFeeInEth);

    if (parseFloat(balanceInEth) >= parseFloat(gasFeeInEth)) {
      console.log('Sufficient balance to cover transaction fee.');
    } else {
      console.log('Insufficient balance to cover transaction fee.');
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// 调用异步函数
checkBalanceAndGas();
