# Blockchain Boosting Trustworthy AI

Django Application that uses Ethereum Blockchain to submit data against a ML model,  provide feedback on various aspects of the data and reward top data submissions.

## Install Dependencies

### Installing the Solidity Compiler

**For OSX**
Install a these homebrew packages:
```
brew install pkg-config libffi autoconf automake libtool openssl
```
Install the solidity compiler (solc):
```
brew update
brew upgrade
brew tap ethereum/ethereum
brew install solidity
brew link solidity
```
**For Linux**
```
sudo add-apt-repository ppa:ethereum/ethereum
sudo apt-get update
sudo apt-get install solc libssl-dev
```

### Firstly you need to install Geth
  [Geth](https://github.com/ethereum/go-ethereum/wiki/geth) is a multipurpose command line tool that runs a full Ethereum node implemented in Go. It offers three interfaces: the command line subcommands and options, a Json-rpc server and an interactive console.

  To install Geth type in the following command in terminal.
  You can also use a one-line script install Geth. Open a command line or terminal tool and paste the command below:
  ```
  bash <(curl -L https://install-geth.ethereum.org)
  ```
  This will detect your OS and will attempt to install the ethereum CLI.
  Also the OS specific installations

  **For OSX**
  Install a these homebrew packages:
  ```
  brew tap ethereum/ethereum
  brew install ethereum
  brew install ethereum --devel
  ```
  **For Linux**
  ```
  sudo apt-get install software-properties-common
  sudo add-apt-repository -y ppa:ethereum/ethereum
  sudo apt-get update
  sudo apt-get install ethereum
  ```


### Initialize your Virtual Environment

Install [virtualenv](https://virtualenv.pypa.io/en/stable/) if you don't have it yet. (Comes installed with [Python3.6](https://www.python.org/downloads/))
Note: Python3.6 or lower is required, One of the packages tensorflow doesn't currently work with Python3.7

Setup a virtual environment with Python 3:
```
cd trustML;
python3.6 -m venv venv;
source venv/bin/activate;
```
### Install python dependencies
  Type the following command in the terminal to install the python libraries:
  ```
  pip3 install -r requirements.txt
  ```

## Run Application

### Run the Blockchain
You will need to run the Geth to run a blockchain locally for the application to connect to.

The blockchain.sh script connects sets up the geth blockchain with its required commands
Type in the following command in terminal:
 ```
 bash blockchain.sh
 ```
### Deploy Contract and Run Django
Open another terminal and make sure you are in the directory containg the main.py file.


 Note: If the contract has already been deployed, you won't need to deploy it again just move to the next step.
 Run the bash script to deploy the smart contract :
 ```
 bash deploy_contract.sh
 ```
 Run the bash script to run Django Application :
 ```
 bash run.sh
 ```
 Open the link running the application on http://127.0.0.1:8000/

## Run Tests
Run the blockchain
```
bash blockchain.sh
```
In a different terminal change into the directory containing all the tests in terminal. Type in the following command:
```
bash run_test.sh
```
This will run all the tests and give feedback on which ones where sucessfull and any which failed.
