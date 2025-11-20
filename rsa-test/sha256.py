import hashlib


def hash(message: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.encode('utf-8'))
    return sha256_hash.hexdigest()


def hash_int(message: int) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(message.to_bytes((message.bit_length() + 7) // 8, 'big'))
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    print(hash("hello"))