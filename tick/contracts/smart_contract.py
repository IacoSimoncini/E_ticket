from web3 import Web3, contract
from web3.middleware import geth_poa_middleware
import json
import random,string

def create_account(w3):
    '''
    Create a new ethereum account
    Parameters:
        w3
    Return:
        acc.address: account's address
        acc.privateKey: account's private key
    '''
    acc = w3.eth.account.create()
    send_wei(w3, w3.eth.coinbase, acc.address)
    return acc.address, acc.privateKey

def send_wei(w3, sender, receiver):
    w3.eth.send_transaction({
        'to': receiver,
        'from': sender,
        'value': w3.toWei('0.5', 'ether')
    })


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

#bisogna resettare anche i ticket
def update_contract(contract_event,num_ticket,nome,luogo,prezzo,w3):
    deploy_txn = contract_event.functions.setValues(num_ticket,nome,luogo,prezzo).transact()
    txn_receipt = w3.eth.get_transaction_receipt(deploy_txn)
    return txn_receipt['to']

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

def hash_receipt(contract_not_deployed, w3, id, num_ticket,nome,luogo,prezzo):
    tx_hash = contract_not_deployed.constructor(id, num_ticket,nome,luogo,prezzo).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash,tx_receipt


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
        address=tx_receipt,
        abi=abi
    )    
    return deployed_contract

def getNameEvent(contract_deployed):
    return contract_deployed.functions.getNameEvent().call()

def getTicketAvaiable(contract_deployed):
    return contract_deployed.functions.getNumTicketsAvailable().call()

def create_ticket(contract_deployed,buyer,taxSeal):
    return contract_deployed.functions.createTicket(buyer,taxSeal).transact()

def buy_ticket(contract_deployed,buyer, w3):
    taxSeal=taxSeal_generator()
    deploy_txn = contract_deployed.functions.buyTicket(buyer,taxSeal).transact()
    txn_receipt = w3.eth.get_transaction_receipt(deploy_txn)
    return txn_receipt['to']

def invalidation(contract_deployed,owner,relative_ID,w3):
    deploy_txn =contract_deployed.functions.invalidation(owner,relative_ID).transact()
    txn_receipt = w3.eth.get_transaction_receipt(deploy_txn)
    return txn_receipt['to']

def delete_event(contract_deployed,event_id,w3):
    deploy_txn=contract_deployed.functions.deleteEvent(event_id).transact()
    txn_receipt = w3.eth.get_transaction_receipt(deploy_txn)
    return txn_receipt['to']

def getTickets(contract_deployed, owner):    
    return contract_deployed.functions.getTickets(owner).call()

def getSoldTickets(contract_deployed):
    return contract_deployed.functions.getSoldTickets().call()

def refundTicket(contract_deployed,owner,relative_ID,w3):
    deploy_txn =contract_deployed.functions.refundTicket(owner,relative_ID).transact()
    txn_receipt = w3.eth.get_transaction_receipt(deploy_txn)
    return txn_receipt['to']

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



def taxSeal_generator():
    x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return x
