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


    def test_getTotalSubmissions(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy = 60
        data_Precision = 70
        data_Recall = int((data_Accuracy+data_Precision)/2)
        data_Fscore = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()
        print("testing get total submission")

        assert res == 1

    def test_getTotalSubmissions2(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy = 45
        data_Precision = 70
        data_Recall = int((data_Accuracy+data_Precision)/2)
        data_Fscore = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 2

    def test_getTotalSubmissions3(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy = 45
        data_Precision = 70
        data_Recall = int((data_Accuracy+data_Precision)/2)
        data_Fscore = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 3

    def test_getTotalSubmissions4(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy = 45
        data_Precision = 70
        data_Recall = int((data_Accuracy+data_Precision)/2)
        data_Fscore = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 5

    def test_getTotalSubmissions4(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy = 45
        data_Precision = 70
        data_Recall = int((data_Accuracy+data_Precision)/2)
        data_Fscore = 60
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        #Submit the Results
        for i in range(10):
            tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
            tx_hash = tx_hash.transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 10




if __name__ == '__main__':
    unittest.main()
