from sympy import randprime
import math
import secrets


class Pubkey:
    def __init__(self, n, e):
        self.n = n
        self.e = e

class Privkey:
    def __init__(self, n, d):
        self.n = n
        self.d = d


def choose_ed(phi):
    while True:
        e = secrets.randbelow(phi - 3) + 3  # in [3, phi-1]
        if e % 2 == 0:
            continue
        if math.gcd(e, phi) == 1:
            break

    d = pow(e, -1, phi) 
    return e, d


p = randprime(2**511, 2**512)
q = randprime(2**512, 2**513)
n = p * q
phi = (p - 1) * (q - 1)
e, d = choose_ed(phi)

pubkey = Pubkey(n, e)
privkey = Privkey(n, d)
maxlen = (n.bit_length() - 1) // 8


def encrypt(message: str, pubkey: Pubkey) -> int:
    if len(message) > maxlen:
        raise ValueError(f"Message too long.")

    message_int = int.from_bytes(message.encode(), 'big')

    return pow(message_int, pubkey.e, pubkey.n)  # computes M^e % n efficiently


def decrypt(ciphertext: int, privkey: Privkey) -> str:
    decrypted_int = pow(ciphertext, privkey.d, privkey.n)  # computes C^d % n efficiently
    decrypted_bytes = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')
    return decrypted_bytes.decode()


message = "Hello, world!"
ciphertext = encrypt(message, pubkey)
print(ciphertext)
decrypted_message = decrypt(ciphertext, privkey)
print(decrypted_message)

