const { Web3 } = require('web3');

// 替换为你的以太坊节点 URL
const nodeUrl = 'http://127.0.0.1:2024';

const web3 = new Web3(nodeUrl);

// 查询节点同步状态
web3.eth.isSyncing()
  .then(syncStatus => {
    if (syncStatus === false) {
      console.log('节点已完全同步');
    } else {
      console.log('节点正在同步中');
      console.log(syncStatus);
    }
  })
  .catch(error => {
    console.error('查询同步状态时出错:', error);
  });
