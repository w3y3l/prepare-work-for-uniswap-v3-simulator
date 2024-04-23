// const { expect } = require("chai");
// const { ethers } = require("hardhat");

// // 闪电交易机器人测试用例
// // 注：需要在 fork 的 Polygon 主网执行用例
// // 执行命令：hh --network localhost test
// describe("FlashBot", function () {

//     let flashBot;
//     let owner;
//     let addr1;
//     let addrs;

//     before(async function () {
//         // 部署机器人合约
//         let FlashBot = await ethers.getContractFactory("FlashBot");
//         flashBot = await FlashBot.deploy();
//         await flashBot.deployed();
//         // 加载测试账户地址
//         [owner, addr1, ...addrs] = await ethers.getSigners();
//         console.log("部署地址 => ", flashBot.address);
//     });


//     it("executeArbitrageSwap", async function () {
//         console.log("钱包地址 => ", owner.address);
//         console.log("钱包余额 => ", await owner.getBalance());
//         let privateKey = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";
//         let wallet = new ethers.Wallet(privateKey, owner.provider);
//         // 加载 WETH 合约
//         let wrapperAddress = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2";
//         let abi = [
//             "function balanceOf(address account) external view returns (uint256)",
//             "function approve(address spender, uint256 amount) external returns (bool)",
//             "function allowance(address owner, address spender) external view returns (uint256)"
//         ];
//         let WETH = new ethers.Contract(wrapperAddress, abi, wallet);
//         let ownerBalance = await WETH.balanceOf(owner.address);
//         console.log("初始 WETH 余额 => ", ownerBalance);
//         // 兑换初始 WETH
//         let amountIn = ethers.BigNumber.from("3841651983176220");
//         if (ownerBalance < amountIn) {
//             let transaction = {
//                 to: wrapperAddress,
//                 value: amountIn.sub(ownerBalance)
//             }
//             await owner.sendTransaction(transaction);
//             ownerBalance = await WETH.balanceOf(owner.address);
//             console.log("补齐 WETH 余额 => ", ownerBalance);
//         }
//         // 授权代币给机器人合约
//         await WETH.approve(flashBot.address, amountIn);
//         let allowance = await WETH.allowance(owner.address, flashBot.address);
//         console.log("授权给机器人合约额度 => ", allowance);
//         // 计算预计兑换后余额
//         let param = {
//             amountIn: amountIn,
//             path: [
//                 "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", // WETH
//                 "0x66fd97a78d8854fec445cd1c80a07896b0b4851f", // TOKEN
//                 "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", // TOKEN
//                 "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", // WETH
//             ],
//             router: [
//                 "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", // UniswapV2Router02
//                 "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", // UniswapV2Router02
//                 "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", // UniswapV2Router02
//             ]
//         }
//         let amountOut = await flashBot.computeSwapAmountOut(param);
//         console.log("预计兑换后 WETH 数量 => ", amountOut);
//         // 执行兑换
//         await flashBot.executeArbitrageSwap(param);
//         ownerBalance = await WETH.balanceOf(owner.address);
//         console.log("兑换后 WETH 数量 => ", ownerBalance);
//         expect(amountOut).to.equal(ownerBalance);
//     });

// });
