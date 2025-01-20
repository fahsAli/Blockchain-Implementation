from blockchain import BlockChain
from wallet import Wallet

blockchain = BlockChain(difficulty=3)

A_wallet = Wallet()
B_wallet = Wallet()
C_wallet = Wallet()

blockchain.register_wallet(A_wallet)
blockchain.register_wallet(B_wallet)
blockchain.register_wallet(C_wallet)

print()

print(f"A's address: {A_wallet.address}")
print(f"B's address: {B_wallet.address}")
print(f"C's address: {C_wallet.address}")

print()

blockchain.initial_distribution[A_wallet.address] = 7000
blockchain.initial_distribution[B_wallet.address] = 2500
blockchain.initial_distribution[C_wallet.address] = 5050

transaction1 = A_wallet.create_transaction(B_wallet.address, 1000)
transaction2 = B_wallet.create_transaction(C_wallet.address, 500)
transaction3 = C_wallet.create_transaction(A_wallet.address, 100)

blockchain.create_transaction(transaction1)
blockchain.create_transaction(transaction2)
blockchain.create_transaction(transaction3)

blockchain.mine_pending_transactions(A_wallet.address)

transaction4 = A_wallet.create_transaction(B_wallet.address, 100)
transaction5 = B_wallet.create_transaction(C_wallet.address, 50)
transaction6 = C_wallet.create_transaction(A_wallet.address, 10)

blockchain.create_transaction(transaction4)
blockchain.create_transaction(transaction5)
blockchain.create_transaction(transaction6)

blockchain.mine_pending_transactions(A_wallet.address)

print(f"A's balance: {blockchain.get_balance(A_wallet.address)}")
print(f"B's balance: {blockchain.get_balance(B_wallet.address)}")
print(f"C's balance: {blockchain.get_balance(C_wallet.address)}")

print()

for block in blockchain.chain:
    print(block)

print()