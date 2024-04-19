import hashlib


def hash_password(in_password: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(in_password.encode('utf-8'))

    md5 = hashlib.md5()
    md5.update(sha256.digest())
    for i in range(0, 128):
        md5.update(md5.digest())

    sha256.update(md5.digest())
    return sha256.hexdigest()


def verify_password(in_password: str, in_hash: str) -> bool:
    return hash_password(in_password) == in_hash
