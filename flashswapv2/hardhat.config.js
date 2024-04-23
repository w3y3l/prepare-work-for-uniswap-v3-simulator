require('dotenv').config()
require("@nomiclabs/hardhat-waffle");

// This is a sample Hardhat task. To learn how to create your own go to
// https://hardhat.org/guides/create-task.html
task("accounts", "Prints the list of accounts", async (taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();

  for (const account of accounts) {
    console.log(account.address);
  }
});

// You need to export an object to set up your config
// Go to https://hardhat.org/config/ to learn more

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: {
    version: "0.8.4",
    settings: {
      optimizer: {
        enabled: false,
        runs: 200
      }
    }
  },
  networks: {
    hardhat: {
      forking: {
        // url: "https://eth-mainnet.g.alchemy.com/v2/ARfXMsoV6ZzkZoFDWZyT-oL3Y2CMdAID",
        url:"http://127.0.0.1:2024" // 主网节点URL
        // blockNumber: 17012051 // 可选，指定从哪个区块开始fork
      },
      accounts: [
        {
          privateKey: '0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80',
          balance: '10000000000000000000' // 设置初始余额，单位为wei
        }
      ]
    }
  }
};
