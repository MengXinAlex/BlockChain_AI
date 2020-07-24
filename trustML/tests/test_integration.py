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


    def test_Accuracy(self):
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
        res = user.functions.getAccuracy(0,w3.eth.accounts[1]).call()
        print("testing get accuracy")
        assert res == data_Accuracy

    def test_Precision(self):
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
        res = user.functions.getPrecision(0,w3.eth.accounts[1]).call()
        print("testing get precision")
        assert res == data_Precision

    def test_Recall(self):
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
        res = user.functions.getRecall(0,w3.eth.accounts[1]).call()
        print("testing get Recall")
        assert res == data_Recall

    def test_getRank(self):
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
        for i in range(10):
            tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
            tx_hash = tx_hash.transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 10

    def test_getSubmission(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy1 = 45
        data_Precision1 = 88
        data_Recall1 = int((data_Accuracy1+data_Precision1)/2)
        data_Fscore1 = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy1,data_Precision1,data_Recall1,data_Fscore1,60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        res1 = user.functions.getSubmission(0,0).call()

        data_Accuracy2 = 64
        data_Precision2 = 23
        data_Recall2 = int((data_Accuracy2+data_Precision2)/2)
        data_Fscore2 = 98
        #Submit the Results
        tx_hash = user.functions.submitData(0,w3.eth.accounts[2],data_Accuracy2,data_Precision2,data_Recall2,data_Fscore2,60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res2 = user.functions.getSubmission(0,1).call()

        assert res1 == [data_Accuracy1,data_Precision1,data_Recall1,data_Fscore1,60]
        assert res2 == [data_Accuracy2,data_Precision2,data_Recall2,data_Fscore2,60]

    def test_multi_differentAcount_getSubmissionAccount(self):
        #Set default account
        contract_address, abi = utils.deploy_n_transact(['../contracts/submission.sol'])
        w3.eth.defaultAccount = w3.eth.accounts[1]
        # Create the contract instance with the newly-deployed address
        user = w3.eth.contract(
            address=contract_address, abi=abi,
        )
        # user.functions.getAccuracy(address).call()
        data_Accuracy1 = 45
        data_Precision1 = 88
        data_Recall1 = int((data_Accuracy1+data_Precision1)/2)
        data_Fscore1 = 60
        #Submit the Results
        for i in w3.personal.listAccounts:
            w3.personal.unlockAccount(i, '', 15000)
        tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy1,data_Precision1,data_Recall1,data_Fscore1,60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)

        data_Accuracy2 = 64
        data_Precision2 = 23
        data_Recall2 = int((data_Accuracy2+data_Precision2)/2)
        data_Fscore2 = 98
        #Submit the Results
        tx_hash = user.functions.submitData(0,w3.eth.accounts[2],data_Accuracy2,data_Precision2,data_Recall2,data_Fscore2,60)
        tx_hash = tx_hash.transact()
        w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res1 = user.functions.getSubmissionAccount(0,0).call()
        res2 = user.functions.getSubmissionAccount(0,1).call()

        assert res1 == w3.eth.accounts[1]
        assert res2 == w3.eth.accounts[2]

    def test_getTotalSubmissions(self):
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
        for i in range(10):
            tx_hash = user.functions.submitData(0,w3.eth.accounts[1],data_Accuracy,data_Precision,data_Recall,data_Fscore, 60)
            tx_hash = tx_hash.transact()
            w3.eth.waitForTransactionReceipt(tx_hash)
        #Store results retrieved from Blockchain and send to data_evaluation page
        res = user.functions.getTotalSubmissions(0).call()

        assert res == 10



if __name__ == '__main__':
    unittest.main()
