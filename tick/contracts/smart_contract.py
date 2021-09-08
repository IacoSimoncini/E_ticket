from web3 import Web3, contract
from web3.middleware import geth_poa_middleware
import json

def start_web3():
    '''
    Start connection with the provider
    Returns:
        w3: Web3 object
    '''
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:22000'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def create_contract(abi, bytecode, w3):
    '''
    Create contract using abi and bytecode
    Parameters:
        abi
        bytecode
        w3
    Returns:
        contract_not_deployed: w3.eth.contract type
    '''
    contract_not_deployed = w3.eth.contract(abi=abi, bytecode=bytecode)
    return contract_not_deployed

def hash_receipt(contract_not_deployed, w3):
    '''
    Hash and receipt of a contract without parameters
    Parameters:
        contract_not_deployed
        w3
    Returns:
        tx_hash: transaction hash
        tx_receipt: info about transaction 
    '''
    tx_hash = contract_not_deployed.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash, tx_receipt



def deploy_contract(tx_receipt, abi, w3):
    '''
    Deploy a contract
    Parameters:
        tx_receipt: receipt of the transaction
        abi
        w3
    Returns:
        deployed_contract: deployed contract
    '''
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
