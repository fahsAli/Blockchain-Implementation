import hashlib
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import base64

class Wallet:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
        
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.address = hashlib.sha256(public_bytes).hexdigest()[:40]
    
    def create_transaction(self, receiver_address, amount):
        transaction = {
            "sender": self.address,
            "receiver": receiver_address,
            "amount": amount,
        }
        
        signature = self.sign_transaction(transaction)
        transaction["signature"] = signature
        return transaction
    
    def sign_transaction(self, transaction):
        tx_copy = transaction.copy()
        if "signature" in tx_copy:
            del tx_copy["signature"]
            
        tx_bytes = json.dumps(tx_copy, sort_keys=True).encode()
        
        signature = self.private_key.sign(
            tx_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')

    def get_public_key_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

