// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

/// @title FlashBot Interface Definition
interface IFlashBot {

    /**************************************************************************
     *                              Aggregated Information Queries            *
     **************************************************************************/

    /**
     * Liquidity Pool Information
     */
    struct PairInfo {
        // Liquidity pool contract
        address pairAddress;
        // token0 contract
        address token0Address;
        // token1 contract
        address token1Address;
        // token0 symbol
        string token0Symbol;
        // token1 symbol
        string token1Symbol;
        // token0 reserve
        uint112 reserve0;
        // token1 reserve
        uint112 reserve1;
    }

    /**
     * @notice Query liquidity pool information
     * @param factoryAddress Factory contract address
     * @param index Liquidity pool index
     */
    function getPairInfo(address factoryAddress, uint256 index) external view returns (PairInfo memory);

    /**
     * @notice Batch query liquidity pool information
     * @param factoryAddress Factory contract address
     * @param startIndex Starting index (inclusive)
     * @param endIndex Ending index (inclusive)
     */
    function batchPairInfo(address factoryAddress, uint256 startIndex, uint256 endIndex) external view returns (PairInfo[] memory);

    /**************************************************************************
     *                                 Execute Arbitrage                      *
     **************************************************************************/

    /**
     * Swap Parameters
     */
    struct SwapParam {
        // Input amount
        uint256 amountIn;
        // Swap path
        address[] path;
        // Router contracts
        address[] router;
    }

    /**
     * @notice Calculate multi-router exchange amounts
     * @param param Swap parameters
     */
    function computeSwapAmountsOut(SwapParam calldata param) external view returns (uint256[] memory);

    /**
     * @notice Calculate final output amount of multi-router exchange
     * @param param Swap parameters
     */
    function computeSwapAmountOut(SwapParam calldata param) external view returns (uint256);

    /**
     * @notice Batch calculate final output amounts of multi-router exchange
     * @param paramList List of swap parameters
     */
    function batchSwapAmountOut(SwapParam[] calldata paramList) external view returns (uint256[] memory);

    /**
     * @notice Execute a swap (msg.sender must have the principal and authorization in advance)
     * @param param Swap parameters
     */
    function executeSwap(SwapParam calldata param) external;

    /**
     * @notice Execute arbitrage swap (msg.sender must have the principal and authorization in advance)
     * @param param Swap parameters
     */
    function executeArbitrageSwap(SwapParam calldata param) external;

    /**
     * @notice Execute a flash swap (no principal required)
     * @param param Swap parameters
     */
    function executeFlashSwap(SwapParam calldata param) external;

    /**
     * @notice Execute arbitrage flash swap (no principal required)
     * @param param Swap parameters
     */
    function executeArbitrageFlashSwap(SwapParam calldata param) external;

    /**************************************************************************
     *                                   Withdrawals                          *
     **************************************************************************/

    /**
     * @notice Withdraw contract balance to owner
     */
    function withdraw() external;

    /**
     * @notice Withdraw contract balance to a specified address
     * @param to Recipient address
     */
    function withdrawTo(address to) external;

    /**
     * @notice Withdraw token balance to owner
     * @param tokens List of tokens
     */
    function withdrawToken(address[] calldata tokens) external;

    /**
     * @notice Withdraw token balance to owner
     * @param tokens List of tokens
     * @param to Recipient address
     */
    function withdrawToken(address[] calldata tokens, address to) external;
}
