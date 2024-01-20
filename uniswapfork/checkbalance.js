
const {Web3} = require('web3');
const NODE_ENDPOINT = 'http://127.0.0.1:2024';  

// 创建web3实例
const web3 = new Web3(new Web3.providers.HttpProvider(NODE_ENDPOINT));

// 定义账户地址
const account = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266';

// 创建一个异步函数以使用await
async function checkBalance() {
    try {
        // 获取账户的余额
        const balance = await web3.eth.getBalance(account);
        console.log('Balance:', web3.utils.fromWei(balance, 'ether'), 'ETH');
        
        // 获取当前的gas价格
        const gasPrice = await web3.eth.getGasPrice();
        console.log('Current Gas Price:', web3.utils.fromWei(gasPrice, 'gwei'), 'gwei');
    } catch (err) {
        console.error('An error occurred:', err);
    }
}

// 调用异步函数
checkBalance();