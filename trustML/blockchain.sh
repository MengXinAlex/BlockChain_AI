#!/bin/sh
geth --dev --cache=1024 --rpc --rpcaddr "127.0.0.1" --rpcport "8545" --rpcapi "web3,eth,personal,admin,debug,miner" --datadir "./blockchain/devchain" --port "30312" --networkid 987 --nat "any" --password="./blockchain/password.txt" console
