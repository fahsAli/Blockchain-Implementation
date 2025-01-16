# Blockchain-Implementation

This project is a simple implementation of a blockchain system, including blocks, transactions, wallets, and a blockchain network. It demonstrates the basic concepts of blockchain technology, such as mining, transaction verification, and wallet management.

## Dependencies

To run this project, you need to install the following Python packages:

```bash
    pip install cryptography
```

## Project Structure

* **block\.py:** Defines the `Block` class, which represents a block in the blockchain. Each block contains an index, timestamp, list of transactions, previous block hash, nonce, and its own hash.

* **blockchain\.py:** Defines the `BlockChain` class, which manages the chain of blocks, pending transactions, and wallet balances. It also handles mining and transaction verification.

* **transaction\.py:** Defines the `Transaction` class, which provides a static method to verify the signature of a transaction.

* **wallet\.py:** Defines the `Wallet` class, which represents a user's wallet. It generates a pair of cryptographic keys (private and public), creates transactions, and signs them.