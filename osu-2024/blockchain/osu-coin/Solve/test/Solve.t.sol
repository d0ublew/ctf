// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.17;

import "forge-std/Test.sol";
import "../src/Setup.sol";

contract SolveTest is Test {
    address player = makeAddr("player");
    Setup public s;

    function setUp() public {
        s = new Setup{value: 100 wei}();
    }

    function testSolve() public {
        vm.startPrank(player);
        OsuCoin coin = OsuCoin(s.coin());

        emit log("before");
        emit log_named_uint("player", coin.balanceOf(player));
        coin.transfer(address(s), player, 100);
        emit log("after");
        emit log_named_uint("player", coin.balanceOf(player));
        emit log_named_uint("setup", coin.balanceOf(address(s)));

        assertEq(s.isSolved(), true);
        vm.stopPrank();
    }
}
