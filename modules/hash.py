import hashlib
from enum import Enum
from pathlib import Path


class HashAlgorithm(Enum):
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"


HASHES = {
    HashAlgorithm.MD5: hashlib.md5,
    HashAlgorithm.SHA1: hashlib.sha1,
    HashAlgorithm.SHA256: hashlib.sha256,
    HashAlgorithm.SHA512: hashlib.sha512,
    HashAlgorithm.BLAKE2B: hashlib.blake2b,
    HashAlgorithm.BLAKE2S: hashlib.blake2s,
}


def _(name: HashAlgorithm = HashAlgorithm.SHA256):
    return HASHES[name]()

def text(text: str, algo: HashAlgorithm) -> str:
    func = _(algo)
    func.update(text.encode())
    return func.hexdigest()

def file(path: Path, algo: HashAlgorithm) -> str:
    func = _(algo)
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(1024)
            if chunk == b"":
                break

        func.update(chunk)
    return func.hexdigest()

def text_compare(string: str, hash: str, algo: HashAlgorithm) -> bool:
    hash1 = text(string, algo)
    return hash1 == hash

def file_compare(file1: Path, hash: str | Path, algo: HashAlgorithm) -> bool:
    fh = Path(hash)
    f = file(file1, algo)

    if fh.is_file():
        hf = file(fh, algo)

        return f == hf

    return f == hash
