import hashlib


def hash_password(in_password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(in_password.encode('utf-8'))

    ripemd160 = hashlib.md5()
    ripemd160.update(sha256.digest())
    for i in range(0, 128):
        ripemd160.update(ripemd160.digest())

    sha256.update(ripemd160.digest())
    return sha256.hexdigest()


def verify_password(in_password: str, in_hash: str) -> bool:
    return hash_password(in_password) == in_hash
