# Notes

## Local Testing

### Setup Test Network

```console
$ anvil
```

### Deploy Contract

```console
$ forge create --rpc-url http://localhost:8545 --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 src/Setup.sol:Setup --value 1ether
[⠊] Compiling...
No files changed, compilation skipped
Deployer: 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720
Deployed to: 0x700b6A60ce7EaaEA56F065753d8dcB9653dbAD35
Transaction hash: 0xaa943b7a5bca82fec4f293f362288cf348fc106d87668b0b11f2ae89cd812685

$ cast call 0x700b6A60ce7EaaEA56F065753d8dcB9653dbAD35 --rpc-url http://localhost:8545 --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 "TARGET()(address)"
0xA44B9f3F5Bb8C278c1ee85D8F32517c6EFa64B0D

$ cast call 0xA44B9f3F5Bb8C278c1ee85D8F32517c6EFa64B0D --rpc-url http://localhost:8545 --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 "debugTxOrigin()(address)"
0xa0Ee7A142d267C1f36714E4a8F75612F20a79720

$ cast call 0xA44B9f3F5Bb8C278c1ee85D8F32517c6EFa64B0D --rpc-url http://localhost:8545 --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 "debugMsgSender()(address)"
0xa0Ee7A142d267C1f36714E4a8F75612F20a79720

$ cast call 0xA44B9f3F5Bb8C278c1ee85D8F32517c6EFa64B0D --rpc-url http://localhost:8545 --private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 "isOffBalance()(bool)"
false
```

### Solving

```sh
# on-chain simulation
SETUP_ADDR=0x700b6A60ce7EaaEA56F065753d8dcB9653dbAD35 forge script script/Solve.s.sol --rpc-url http://localhost:8545

# solve locally
SETUP_ADDR=0x700b6A60ce7EaaEA56F065753d8dcB9653dbAD35 forge script script/Solve.s.sol --rpc-url http://localhost:8545 --broadcast
```
