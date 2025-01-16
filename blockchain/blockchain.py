from block import Block
from transaction import Transaction

class BlockChain:
    def __init__(self, difficulty=3):
        self.chain = self.create_genesis_block()
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 1
        self.wallets = {}
        self.initial_distribution = {}
        
    def create_genesis_block(self):
        return [Block(index=0, previous_hash="0", transactions=[], nonce=0)]

    def get_latest_block(self):
        return self.chain[-1]
        
    def register_wallet(self, wallet):
        self.wallets[wallet.address] = wallet.get_public_key_bytes()

    def get_balance(self, address):
        balance = 0
        
        if address in self.initial_distribution:
            balance += self.initial_distribution[address]
            
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == address:
                    balance -= transaction["amount"]
                if transaction["receiver"] == address:
                    balance += transaction["amount"]
        
        for transaction in self.pending_transactions:
            if transaction["sender"] == address:
                balance -= transaction["amount"]
            if transaction["receiver"] == address:
                balance += transaction["amount"]
                
        return balance

    def verify_transaction(self, transaction):
        sender = transaction["sender"]
        amount = transaction["amount"]
        
        if sender == "System":
            return True
            
        sender_balance = self.get_balance(sender)
        return sender_balance >= amount

    def create_transaction(self, transaction):
        required_fields = ["sender", "receiver", "amount", "signature"]
        
        if not all(field in transaction for field in required_fields):
            raise ValueError("Missing required fields in transaction data.")
            
        if transaction["amount"] <= 0:
            raise ValueError("Transaction amount must be positive.")
            
        if transaction["sender"] != "System":
            if transaction["sender"] not in self.wallets:
                raise ValueError("Unknown wallet address")
                
            public_key_bytes = self.wallets[transaction["sender"]]
            if not Transaction.verify_signature(transaction, public_key_bytes):
                raise ValueError("Invalid transaction signature")
            
            if not self.verify_transaction(transaction):
                raise ValueError(f"Insufficient funds. {transaction['sender']} only has {self.get_balance(transaction['sender'])} AC.")
        
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        if not self.pending_transactions:
            raise ValueError("No transactions to mine.")
        
        reward_transaction = {
            "sender": "System",
            "receiver": miner_address,
            "amount": self.mining_reward,
            "signature": "mining_reward"
        }
        self.pending_transactions.append(reward_transaction)

        latest_block = self.get_latest_block()
        
        block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            transactions=self.pending_transactions
        )

        block.mine_block(self.difficulty)
        
        self.chain.append(block)
        self.pending_transactions = []

    def get_transaction_history(self, address):
        transactions = []
        for block in self.chain:
            for tx in block.transactions:
                if tx["sender"] == address or tx["receiver"] == address:
                    transactions.append({
                        "block": block.index,
                        "transaction": tx
                    })
        return transactions

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
                
            if current_block.previous_hash != previous_block.hash:
                return False
                
        return True