from pathlib import Path

from .typings import HASHES, HashAlgorithm


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
