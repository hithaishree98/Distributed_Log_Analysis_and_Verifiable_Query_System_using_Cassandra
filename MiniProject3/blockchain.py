from web3 import Web3
from solcx import compile_source
 
class Blockchain:
    def __init__(self, host):
        self.host = host
        self.contract_id = None
        self.contract_interface = None
        self.abi = None
        self.bytecode = None
        self.contract_instance = None
        self.service_provider = None
 
    def set_merkle_root(self, merkle_root):
        try:
            set_tx_hash = self.contract_instance.functions.setMerkleRoot(merkle_root).transact()
            set_tx_receipt = self.service_provider.eth.wait_for_transaction_receipt(set_tx_hash)
            return set_tx_receipt
        except Exception as e:
            print(f"Failed to set Merkle root: {e}")
            return None
 
    def get_merkle_root(self):
        try:
            return self.contract_instance.functions.getMerkleRoot().call()
        except Exception as e:
            print(f"Failed to retrieve Merkle root: {e}")
            return None
 
    def compile_contract(self):
        compiled_sol = compile_source(
            '''
            pragma solidity ^0.8.0;
            contract Verify {
                string private merkleRoot;
 
                function setMerkleRoot(string memory _merkleRoot) public {
                    merkleRoot = _merkleRoot;
                }
 
                function getMerkleRoot() public view returns (string memory) {
                    return merkleRoot;
                }
            }
            ''',
            output_values=['abi', 'bin']
        )
 
        contract_id, contract_interface = compiled_sol.popitem()
        self.bytecode = contract_interface['bin']
        self.abi = contract_interface['abi']
 
    def deploy_contract(self):
        w3 = Web3(Web3.HTTPProvider(self.host))
        self.service_provider = w3
        w3.eth.default_account = w3.eth.accounts[0]
 
        Verify = w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        deploy_tx_hash = Verify.constructor().transact()
        deploy_tx_receipt = w3.eth.wait_for_transaction_receipt(deploy_tx_hash)
 
        self.contract_instance = w3.eth.contract(
            address=deploy_tx_receipt.contractAddress,
            abi=self.abi
        )