# Local Testing

## Using Test

```
forge test ./test/EasyChallenge.t.sol
```

## Using Script

```sh
anvil

# private key obtained from anvil
forge create ./src/Setup.sol:Setup --rpc-url http://localhost:8545 --private-key ${PRIVATE_KEY} --broadcast

# Get the deployed contract address
export SETUP_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
export PRIVATE_KEY=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
forge script ./script/Solve.s.sol --rpc-url http://localhost:8545 --broadcast
```

# Notes

```sh
forge build

# List available API
cast interface ./out/Setup.sol/Setup.json
cast interface ./out/GuessIt.sol/EasyChallenge.json
```

# References

- https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html#mappings-and-dynamic-arrays
