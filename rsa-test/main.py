import rsa
import sha256
import diffiehellman


def encrypt(message: str, pubkey: rsa.Pubkey, privkey: rsa.Privkey) -> int:
    message_hash = sha256.hash(message)
    rsa_signature = rsa.sign(int(message_hash, 16), privkey)
    ciphertext = rsa.encrypt(message, pubkey)

    return rsa_signature,ciphertext


def decrypt(rsa_signature: int, ciphertext: int, pubkey: rsa.Pubkey, privkey: rsa.Privkey) -> str:
    message = rsa.decrypt(ciphertext, privkey)
    message_hash = sha256.hash(message)
    hash_int = int(message_hash, 16)
    hash_from_signature = pow(rsa_signature, pubkey.e, pubkey.n)

    # we know the message was not tampered with if the hashes match
    if hash_int != hash_from_signature:
        raise ValueError("Signature verification failed.")

    return message


def main():
    alice_pub, alice_priv = rsa.generate_keypair()
    bob_pub, bob_priv = rsa.generate_keypair()



