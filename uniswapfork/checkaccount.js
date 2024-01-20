const {Web3} = require('web3');
const web3 = new Web3('http://127.0.0.1:2024');

const fromAddress = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';
const privateKey = '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80';

// 设置 gas 价格和限制
const gasPrice = '30000000000'; // 30 Gwei
const gasLimit = 21000; // 你的交易所需的 gas 限制

// 构建交易对象
const transactionObject = {
  from: fromAddress,
  to: '0xYourContractAddress', // 合约地址
  gas: gasLimit,
  gasPrice: gasPrice,
  value: '0', // 你要发送的以太币数量
  data: '0xYourEncodedContractData' // 合约函数调用数据
};

// 使用私钥签名交易
web3.eth.accounts.signTransaction(transactionObject, privateKey)
  .then(signedTransaction => {
    // 发送交易
    return web3.eth.sendSignedTransaction(signedTransaction.rawTransaction);
  })
  .then(receipt => {
    console.log('Transaction receipt:', receipt);
  })
  .catch(error => {
    console.error('Transaction error:', error);
  });
