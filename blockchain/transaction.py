import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import base64


class Transaction:
    @staticmethod
    def verify_signature(transaction, public_key_bytes):
        try:
            public_key = serialization.load_pem_public_key(public_key_bytes)
            
            signature = base64.b64decode(transaction["signature"])
            
            tx_copy = transaction.copy()
            del tx_copy["signature"]
            
            tx_bytes = json.dumps(tx_copy, sort_keys=True).encode()
            
            public_key.verify(
                signature,
                tx_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False