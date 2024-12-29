// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/GuessIt.sol";
import "../src/Setup.sol";

contract EasyChallengeTest is Test {
    EasyChallenge easyChallenge;
    Setup setup;

    function setUp() public {
        setup = new Setup();
        easyChallenge = setup.challengeInstane();
    }

    function testUnlock() public {
        // Calculate the storage slot for keys[0x1337]
        uint256 slot = uint256(keccak256(abi.encodePacked(uint(0x1337), uint(1))));

        // Call the unlock function with the correct slot
        easyChallenge.unlock(slot);

        // Assert that the key was found
        assertTrue(easyChallenge.isKeyFound());
    }
}

