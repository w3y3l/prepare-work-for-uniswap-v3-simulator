const {Web3} = require('web3');

// 初始化 Web3
const web3 = new Web3('http://127.0.0.1:2024'); // 替换为您的 Ethereum 节点 URL

// WETH 合约地址和 ABI
const wethAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'; // WETH 合约地址
const wethAbi = [{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"}, /* ... 其他函数 ... */];

// 您的账户地址
const myAccount = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'; // 替换为您的账户地址

// 创建 WETH 合约实例
const wethContract = new web3.eth.Contract(wethAbi, wethAddress);

// 设置要转换的 ETH 数量（例如，转换 0.5 ETH）
const amountOfEthToConvert = web3.utils.toWei('0.5', 'ether'); // 转换为 wei

// 创建交易对象
const depositTransaction = {
    from: myAccount,
    to: wethAddress,
    value: amountOfEthToConvert, // 转换的 ETH 数量，以 wei 为单位
    data: wethContract.methods.deposit().encodeABI() // 调用 WETH 合约的 deposit 方法
};

// 发送交易
web3.eth.sendTransaction(depositTransaction)
  .then(receipt => {
      console.log('交易收据:', receipt);
  })
  .catch(error => {
      console.error('交易失败:', error);
  });
