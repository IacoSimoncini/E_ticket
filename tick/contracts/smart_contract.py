from web3 import Web3, contract
from web3.middleware import geth_poa_middleware
import json

def start_web3():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:22000'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def create_contract(abi, bytecode, w3):
    contract_not_deployed = w3.eth.contract(abi=abi, bytecode=bytecode)
    return contract_not_deployed

def deploy_contract(contract_not_deployed, tx_receipt, abi, w3):
    deployed_contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )    
    return deployed_contract

def read_abi(abi_name):
    with open(abi_name) as jsonFile:
        abi = json.load(jsonFile)
        jsonFile.close()

    return abi

def read_bytecode(bytecode_name):
    with open(bytecode_name) as jsonFile:
        bytecode = json.load(jsonFile)
        jsonFile.close()
    
    return bytecode["object"]
