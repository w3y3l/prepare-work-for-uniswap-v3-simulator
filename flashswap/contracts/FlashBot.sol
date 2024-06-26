//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import "hardhat/console.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

import "./interfaces/IFlashBot.sol";
import "./interfaces/IUniswapV2Callee.sol";
import "./interfaces/IUniswapV2Factory.sol";
import "./interfaces/IUniswapV2Pair.sol";
import "./interfaces/IUniswapV2Router02.sol";
import "./libraries/UniswapV2Library.sol";
import "./libraries/SafeCall.sol";

/// @title 闪电机器人接口实现
contract FlashBot is IFlashBot, IUniswapV2Callee, Ownable {
    using SafeMath for uint;

    fallback() external payable {}

    receive() external payable {}

    /// @inheritdoc IFlashBot
    function getPairInfo(
        address factoryAddress,
        uint256 index
    ) public view override returns (PairInfo memory) {
        address pairAddress = IUniswapV2Factory(factoryAddress).allPairs(index);
        address token0Address = IUniswapV2Pair(pairAddress).token0();
        string memory token0Symbol = SafeCall.symbol(token0Address);
        address token1Address = IUniswapV2Pair(pairAddress).token1();
        string memory token1Symbol = SafeCall.symbol(token1Address);
        (uint112 reserve0, uint112 reserve1, ) = IUniswapV2Pair(pairAddress)
            .getReserves();
        return
            PairInfo({
                pairAddress: pairAddress,
                token0Address: token0Address,
                token0Symbol: token0Symbol,
                reserve0: reserve0,
                token1Address: token1Address,
                token1Symbol: token1Symbol,
                reserve1: reserve1
            });
    }

    /// @inheritdoc IFlashBot
    function batchPairInfo(
        address factoryAddress,
        uint256 startIndex,
        uint256 endIndex
    ) external view override returns (PairInfo[] memory) {
        require(endIndex >= startIndex, "INDEX ERROR");
        PairInfo[] memory pairInfoList = new PairInfo[](
            endIndex - startIndex + 1
        );
        for (uint256 i = 0; i < pairInfoList.length; i++) {
            uint256 index = i + startIndex;
            pairInfoList[i] = getPairInfo(factoryAddress, index);
        }
        return pairInfoList;
    }

    /// @inheritdoc IFlashBot
    function computeSwapAmountsOut(
        SwapParam memory param
    ) public view override returns (uint256[] memory) {
        require(param.path.length >= 2, "PATH ERROR");
        require(param.path.length - 1 == param.router.length, "ROUTER ERROR");
        // 计算兑换金额
        uint256[] memory _amounts = new uint256[](param.path.length);
        _amounts[0] = param.amountIn;
        for (uint256 i = 0; i < param.router.length; i++) {
            address[] memory _path = new address[](2);
            _path[0] = param.path[i];
            _path[1] = param.path[i + 1];
            // 通过路由合约计算输出金额
            uint[] memory amounts = IUniswapV2Router02(param.router[i])
                .getAmountsOut(_amounts[i], _path);
            _amounts[i + 1] = amounts[amounts.length - 1];
        }
        return _amounts;
    }

    /// @inheritdoc IFlashBot
    function computeSwapAmountOut(
        SwapParam calldata param
    ) external view override returns (uint256) {
        uint256[] memory amounts = computeSwapAmountsOut(param);
        // 依次检查每步实际是否可兑换 防止无法兑换白白消耗 Gas 费
        // 对于无法转账的代币 以下校验规则拦不住 因为下面"amountIn"有值 而实际没有 所以只能在数据库里把代币拉黑
        for (uint256 i = 0; i < param.router.length; i++) {
            (address input, address output) = (
                param.path[i],
                param.path[i + 1]
            );
            (address token0, ) = UniswapV2Library.sortTokens(input, output);
            (uint256 amount0In, uint256 amount1In) = input == token0
                ? (amounts[i], uint256(0))
                : (uint256(0), amounts[i]);
            (uint256 amount0Out, uint256 amount1Out) = input == token0
                ? (uint256(0), amounts[i + 1])
                : (amounts[i + 1], uint256(0));
            address pairAddress = _getPairAddress(
                param.router[i],
                input,
                output
            );
            (uint112 _reserve0, uint112 _reserve1, ) = IUniswapV2Pair(
                pairAddress
            ).getReserves();
            require(
                amount0Out < _reserve0 && amount1Out < _reserve1,
                "FlashBot: INSUFFICIENT_LIQUIDITY"
            );
            uint balance0;
            uint balance1;
            {
                // scope for _token{0,1}, avoids stack too deep errors
                balance0 =
                    IERC20(IUniswapV2Pair(pairAddress).token0()).balanceOf(
                        pairAddress
                    ) +
                    amount0In -
                    amount0Out;
                balance1 =
                    IERC20(IUniswapV2Pair(pairAddress).token1()).balanceOf(
                        pairAddress
                    ) +
                    amount1In -
                    amount1Out;
            }
            {
                // scope for reserve{0,1}Adjusted, avoids stack too deep errors
                uint balance0Adjusted = balance0.mul(1000).sub(
                    amount0In.mul(3)
                );
                uint balance1Adjusted = balance1.mul(1000).sub(
                    amount1In.mul(3)
                );
                require(
                    balance0Adjusted.mul(balance1Adjusted) >=
                        uint(_reserve0).mul(_reserve1).mul(1000 ** 2),
                    "FlashBot: K"
                );
            }
        }
        return amounts[amounts.length - 1];
    }

    /// @inheritdoc IFlashBot
    function batchSwapAmountOut(
        SwapParam[] calldata paramList
    ) external view override returns (uint256[] memory) {
        uint256[] memory amountOutList = new uint256[](paramList.length);
        for (uint256 i = 0; i < paramList.length; i++) {
            try this.computeSwapAmountOut(paramList[i]) returns (
                uint256 amount
            ) {
                amountOutList[i] = amount;
            } catch {
                amountOutList[i] = 0;
            }
        }
        return amountOutList;
    }

    /// @inheritdoc IFlashBot
    function executeSwap(SwapParam calldata param) external override {
        uint256[] memory amounts = computeSwapAmountsOut(param);
        _swap(amounts, param.path, param.router);
    }

    /// @inheritdoc IFlashBot
    function executeArbitrageSwap(SwapParam memory param) public override {
        require(param.path.length >= 3, "PATH ERROR");
        require(
            param.path[0] == param.path[param.path.length - 1],
            "TOKEN ERROR"
        );
        uint256[] memory amounts = computeSwapAmountsOut(param);
        // 判断回来的代币数量要大于支付的数量
        require(amounts[amounts.length - 1] > amounts[0], "NO ARBITRAGE");
        uint256 beforeBalance = IERC20(param.path[0]).balanceOf(address(this));
        _swap(amounts, param.path, param.router);
        // 校验钱包余额 确认套利成功 否则交易revert
        uint256 afterBalance = IERC20(param.path[0]).balanceOf(address(this));
        require(afterBalance > beforeBalance, "ARBITRAGE FAILURE");
    }

    /// @inheritdoc IFlashBot
    function executeFlashSwap(SwapParam calldata param) external override {
        // TODO
    }

    /// @inheritdoc IFlashBot
    function executeArbitrageFlashSwap(
        SwapParam calldata param
    ) external override {
        // TODO
    }

    /// @inheritdoc IUniswapV2Callee
    function uniswapV2Call(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IUniswapV2Callee
    function waultSwapCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IUniswapV2Callee
    function apeCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IUniswapV2Callee
    function jetswapCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IUniswapV2Callee
    function elkCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IUniswapV2Callee
    function cafeCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) external override {
        _flashSwapCall(sender, amount0, amount1, data);
    }

    /// @inheritdoc IFlashBot
    function withdraw() external override onlyOwner {
        withdrawTo(owner());
    }

    /// @inheritdoc IFlashBot
    function withdrawTo(address to) public override onlyOwner {
        require(address(this).balance > 0, "INSUFFICIENT BALANCE");
        payable(to).transfer(address(this).balance);
    }

    /// @inheritdoc IFlashBot
    function withdrawToken(
        address[] calldata tokens
    ) external override onlyOwner {
        withdrawToken(tokens, owner());
    }

    /// @inheritdoc IFlashBot
    function withdrawToken(
        address[] calldata tokens,
        address to
    ) public override onlyOwner {
        for (uint256 i = 0; i < tokens.length; i++) {
            uint256 balance = IERC20(tokens[i]).balanceOf(address(this));
            if (balance > 0) {
                IERC20(tokens[i]).transferFrom(address(this), to, balance);
            }
        }
    }

    function startFlash(SwapParam calldata param) external {
        require(param.path.length >= 3, "PATH ERROR");
        require(
            param.path[0] == param.path[param.path.length - 1],
            "TOKEN ERROR"
        );

        address borrowerToken = param.path[0];
        uint256 borrowerAmount = uint256(param.amountIn);

        address usdtAddress = 0xdAC17F958D2ee523a2206206994597C13D831ec7;
        address shushiRouter = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;

        address pair = 0x06da0fd433C1A5d7a4faa01111c044910A184553;

        (address input, address output) = (borrowerToken, usdtAddress);
        (address token0, ) = UniswapV2Library.sortTokens(input, output);

        if (token0 == borrowerToken) {
            IUniswapV2Pair(pair).swap(
                borrowerAmount,
                0,
                address(this),
                abi.encode(param)
            );
        } else {
            IUniswapV2Pair(pair).swap(
                0,
                borrowerAmount,
                address(this),
                abi.encode(param)
            );
        }

        IERC20(borrowerToken).transfer(msg.sender, IERC20(borrowerToken).balanceOf(address(this)));
    }

    /**
     * @notice 多路由兑换
     * @param amounts 兑换金额
     * @param path 兑换路径
     * @param router 路由合约
     */
    function _swap(
        uint[] memory amounts,
        address[] memory path,
        address[] memory router
    ) internal virtual {
        // 把初始金额转入第一个流动池合约
        address pair = _getPairAddress(router[0], path[0], path[1]);
        IERC20(path[0]).transfer(pair, amounts[0]);
        // 多路由兑换
        for (uint256 i; i < router.length; i++) {
            (address input, address output) = (path[i], path[i + 1]);
            (address token0, ) = UniswapV2Library.sortTokens(input, output);
            uint256 amountOut = amounts[i + 1];
            (uint256 amount0Out, uint256 amount1Out) = input == token0
                ? (uint256(0), amountOut)
                : (amountOut, uint256(0));
            address to = i < router.length - 1
                ? _getPairAddress(router[i + 1], output, path[i + 2])
                : address(this);
            IUniswapV2Pair(_getPairAddress(router[i], input, output)).swap(
                amount0Out,
                amount1Out,
                to,
                new bytes(0)
            );
        }
    }

    /**
     * @notice 闪电兑换执行逻辑
     * @param sender 资金来源 pair 合约
     * @param amount0 借出token0数量
     * @param amount1 借出token1数量
     * @param data 附加数据
     */
    function _flashSwapCall(
        address sender,
        uint amount0,
        uint amount1,
        bytes calldata data
    ) internal {
        if (keccak256(data) != keccak256(new bytes(0))) {
            address token0 = IUniswapV2Pair(msg.sender).token0(); // 获取token0地址
            address token1 = IUniswapV2Pair(msg.sender).token1(); // 获取token1地址

            executeArbitrageSwap(abi.decode(data, (SwapParam)));

            // 计算还款金额和费用
            uint fee = ((amount0 > 0 ? amount0 : amount1) * 3) / 997 + 1;
            uint amountToRepay = (amount0 > 0 ? amount0 : amount1) + fee;

            // 还款给Uniswap V2 pair
            address token = amount0 > 0 ? token0 : token1;
            IERC20(token).transfer(msg.sender, amountToRepay);
        }
    }

    /**
     * @notice 获取流动池合约地址
     * @param router 路由合约
     * @param token0 代币0
     * @param token1 代币1
     */
    function _getPairAddress(
        address router,
        address token0,
        address token1
    ) internal view returns (address) {
        address factory = IUniswapV2Router02(router).factory();
        return IUniswapV2Factory(factory).getPair(token0, token1);
    }
}
