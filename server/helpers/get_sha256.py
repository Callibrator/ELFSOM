#Returns the sha256 of file
import hashlib


def get_sha256(filename):

    sha256_hash = hashlib.sha256()
    sha = ""
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        sha = sha256_hash.hexdigest()

    return sha