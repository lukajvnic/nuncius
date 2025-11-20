from random import randint
from cryptography.hazmat.primitives.asymmetric import dh
import sha256
import rsa

def handshake(privkey=rsa.Privkey):
    parameters = dh.generate_parameters(generator=2, key_size=512)
    p = parameters.parameter_numbers().p
    g = parameters.parameter_numbers().g

    a = randint(2, p - 2)
    A = pow(g, a, p)  # A^b == B^a

    signature = pow(sha256.hash_int(A), privkey.d, privkey.n)
                      
    return {
        "signature": signature,
        "public-dh": A,
        "prime": p
    }


def verify_handshake(signature, public_dh, pubkey: rsa.Pubkey) -> int:
    hash_int = int(sha256.hash_int(public_dh), 16)
    hash_from_signature = pow(signature, pubkey.e, pubkey.n)

    return hash_int == hash_from_signature
