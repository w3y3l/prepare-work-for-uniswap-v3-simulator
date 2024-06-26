// SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol';
import "@openzeppelin/contracts/utils/Address.sol";
import '../interfaces/IUniswapV2Pair.sol';

/**
 * @title Safe external contract calls to prevent failures from reverting the transaction
 */
library SafeCall {
    
    using Address for address;

    /**
     * @notice Query token balance of an account
     * @param tokenAddress The token contract address
     * @param account The wallet address
     */
    function balanceOf(address tokenAddress, address account) internal view returns (uint256) {
        if (!tokenAddress.isContract()) {
            return 0;
        }
        try IERC20Metadata(tokenAddress).balanceOf(account) returns (uint256 value) {
            return value;
        } catch {
            return 0;
        }
    }

    /**
     * @notice Query the allowance of a token for a spender from an account
     * @param tokenAddress The token contract address
     * @param account The wallet address
     * @param spender The address authorized to spend
     */
    function allowance(address tokenAddress, address account, address spender) internal view returns (uint256) {
        if (!tokenAddress.isContract()) {
            return 0;
        }
        try IERC20Metadata(tokenAddress).allowance(account, spender) returns (uint256 value) {
            return value;
        } catch {
            return 0;
        }
    }

    /**
     * @notice Query the name of a token
     * @param tokenAddress The token contract address
     */
    function name(address tokenAddress) internal view returns (string memory) {
        if (!tokenAddress.isContract()) {
            return '';
        }
        try IERC20Metadata(tokenAddress).name() returns (string memory value) {
            return value;
        } catch {
            return '';
        }
    }

    /**
     * @notice Query the symbol of a token
     * @param tokenAddress The token contract address
     */
    function symbol(address tokenAddress) internal view returns (string memory) {
        if (!tokenAddress.isContract()) {
            return '';
        }
        try IERC20Metadata(tokenAddress).symbol() returns (string memory value) {
            return value;
        } catch {
            return '';
        }
    }

    /**
     * @notice Query the decimals of a token
     * @param tokenAddress The token contract address
     */
    function decimals(address tokenAddress) internal view returns (uint8) {
        if (!tokenAddress.isContract()) {
            return 18;
        }
        try IERC20Metadata(tokenAddress).decimals() returns (uint8 value) {
            return value;
        } catch {
            return 18;
        }
    }

    /**
     * @notice Query the total supply of a token
     * @param tokenAddress The token contract address
     */
    function totalSupply(address tokenAddress) internal view returns (uint256) {
        if (!tokenAddress.isContract()) {
            return 0;
        }
        try IERC20Metadata(tokenAddress).totalSupply() returns (uint256 value) {
            return value;
        } catch {
            return 0;
        }
    }

    /**
     * @notice Query the token0 address of a UniswapV2 pair contract
     * @param pairAddress The UniswapV2 pair contract address
     */
    function token0(address pairAddress) internal view returns (address) {
        if (!pairAddress.isContract()) {
            return address(0);
        }
        try IUniswapV2Pair(pairAddress).token0() returns (address value) {
            return value;
        } catch {
            return address(0);
        }
    }

    /**
     * @notice Query the token1 address of a UniswapV2 pair contract
     * @param pairAddress The UniswapV2 pair contract address
     */
    function token1(address pairAddress) internal view returns (address) {
        if (!pairAddress.isContract()) {
            return address(0);
        }
        try IUniswapV2Pair(pairAddress).token1() returns (address value) {
            return value;
        } catch {
            return address(0);
        }
    }

    /**
     * @notice Query the reserve amounts of a UniswapV2 pair contract
     * @param pairAddress The UniswapV2 pair contract address
     */
    function getReserves(address pairAddress) 
        internal 
        view 
        returns (uint112, uint112, uint32) 
    {
        if (!pairAddress.isContract()) {
            return (0, 0, 0);
        }
        try IUniswapV2Pair(pairAddress).getReserves() returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast) {
            return (reserve0, reserve1, blockTimestampLast);
        } catch {
            return (0, 0, 0);
        }
    }
}
