// checknode.js
const { Web3 } = require('web3');
const web3 = new Web3('http://127.0.0.1:2024');
async function checkNodeInfo() {
    try {
      const nodeInfo = await web3.eth.getNodeInfo();
      console.log("Node Info:", nodeInfo);
  
      // 继续执行其他异步代码...
    } catch (error) {
      console.error("An error occurred:", error);
    }
  }
  
  checkNodeInfo();
  