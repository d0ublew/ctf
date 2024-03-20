// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

interface ICreature {
    function aggro() external view returns (address);
    function attack(uint256 _damage) external;
    function lifePoints() external view returns (uint256);
    function loot() external;
    function isOffBalance() external view returns (bool);
    function debugTxOrigin() external view returns (address);
    function debugMsgSender() external view returns (address);
}

contract Attacker {
    ICreature private creature;
    constructor(address instance) {
        creature = ICreature(instance);
    }

    function attack(uint256 dmg) public {
        creature.attack(dmg);
    }

    function isOffBalance() public view returns (bool) {
        return creature.isOffBalance();
    }

    function debugMsgSender() public view returns (address) {
        return creature.debugMsgSender();
    }

    function debugTxOrigin() public view returns (address) {
        return creature.debugTxOrigin();
    }
}
