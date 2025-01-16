import hashlib
import json
import time

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: dict, nonce: int = 0):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_dict = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        hash = self.hash
        while hash[:difficulty] != target:
            self.nonce += 1
            hash = self.calculate_hash()
        self.hash = hash
        return self.hash
    
    def __str__(self):
        id = str(self.index) + ")  Hash: " + self.hash + "\n" + "    Previous Hash: " + self.previous_hash + "\n"
        timestamp = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(self.timestamp))
        id += "    date : " + timestamp + "\n    Transactions:\n"
        transactions = ""
        for trans in self.transactions:
            transactions += "       > " + trans["sender"] + " -> " + trans["receiver"] + " : " + str(trans["amount"]) + " C\n"
        return id + transactions 