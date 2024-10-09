from db_provider import Server
from data_owner import DataOwner
from adv_client import MaliciousClient
from query_client import QueryClient
from blockchain import Blockchain
 
if __name__ == '__main__':
    blockchain = Blockchain('http://127.0.0.1:8545')
    blockchain.compile_contract()
    blockchain.deploy_contract()
 
    data_provider = Server()
    data = {"k1": "a", "k2": "b", "k3": "c"}
 
    data_owner = DataOwner(data, data_provider, blockchain)
    data_owner.build_merkle_tree()
    data_owner.insert_data_to_server()
    data_owner.upload_merkle_root_to_blockchain()
    merkle_tree = data_owner.get_merkle_tree()
 
    query_client = QueryClient(data_provider, blockchain, merkle_tree)
    key = "k1"
    k1_query_value = query_client.query_by_key(key)
    k1_proofs = query_client.retrieve_verification_path_by_tree(list(data.keys()).index(key)) # 0 means root path
 
    # Debugging print to check the Merkle root retrieved from the blockchain
    root_from_contract = blockchain.get_merkle_root()
    print("Merkle root from blockchain:", root_from_contract)
 
    if query_client.query_verification(key, k1_query_value, k1_proofs, root_from_contract):
        print("Retrieved value is verified")
    else:
        print("Retrieved value is modified")