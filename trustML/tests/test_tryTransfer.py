import sys
sys.path.append('../trustML')
import os
import unittest
from solc import link_code
import json
from compile_solidity_utils import w3
import compile_solidity_utils as utils
import numpy as np
from compile_solidity_utils import w3
# Solidity source code



class TestCase(unittest.TestCase):
    def test_reward(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[0]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        sender_address = w3.eth.accounts[1]
        receiver_address = w3.eth.accounts[2]

        w3.personal.unlockAccount(sender_address, '', 15000)
        w3.personal.unlockAccount(receiver_address, '')

        before_sender = w3.eth.getBalance(w3.eth.accounts[1])
        before_receiver = w3.eth.getBalance(w3.eth.accounts[2])
        value = 0.1
        amount = w3.toWei(value, "ether")
        w3.eth.sendTransaction({'from': sender_address, 'to': receiver_address, 'value': amount})
        #print("Sender Balance: {}".format(w3.fromWei(w3.eth.getBalance(sender_address), 'ether')), "Reciever Balance: {}".format(w3.fromWei(w3.eth.getBalance(receiver_address), 'ether')))

        w3.personal.lockAccount(receiver_address)
        w3.personal.lockAccount(sender_address)
        after_sender = w3.eth.getBalance(w3.eth.accounts[1])
        after_receiver = w3.eth.getBalance(w3.eth.accounts[2])
        assert after_receiver == (before_receiver + amount)


if __name__ == '__main__':
    unittest.main()
