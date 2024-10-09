import merkletools
 
class DataOwner:
    def __init__(self, key_value_data, server, blockchain):
        self.data = key_value_data
        self.server = server
        self.blockchain = blockchain
        self.merkle_tree = merkletools.MerkleTools(hash_type='sha256')
 
    def insert_data_to_server(self):
        for key, value in self.data.items():
            self.server.add_data(key, value)
        print("Data inserted to server.")
 
    def build_merkle_tree(self):
        for key, value in self.data.items():
            self.merkle_tree.add_leaf(f"{key}:{value}", True)
        self.merkle_tree.make_tree()
        print("Merkle tree built.")
 
    def upload_merkle_root_to_blockchain(self):
        root = self.merkle_tree.get_merkle_root()
        self.blockchain.set_merkle_root(root)
        print("Merkle root uploaded to blockchain:", root)
 
    def get_merkle_tree(self):
        return self.merkle_tree