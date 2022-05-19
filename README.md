# Disclaimer
This repo is still a work in progress and is currently UNTESTED. I'm pretty sure the write functions will not work as implemented. Please don't use this repo until this disclaimer is removed!

# AAVE-V3-PY
The purpose of this repository is to provide wrapper classes around common Aave contracts that reduce boilerplate code. The classes can be found in the aavev3 folder.

## Quick Start
```
from aavev3 import Pool
from web3 import Web3

test_addr = Web3.toChecksumAddress("0xD5CF5F10f7FEa9aB90D4b7a8F556Db78a9eBDb4B")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
pool_instance = Pool(w3, "polygon")

print(pool_instance.getUserAccountData(test_addr))
```

## More Info
Aave provides extensive documentation on their contracts which can be found [here](https://docs.aave.com/developers/getting-started/v3-overview)

## Dev
Tests are run on a local node with Anvil, which is part of the forge family. More info about forge [here](https://github.com/foundry-rs/foundry)