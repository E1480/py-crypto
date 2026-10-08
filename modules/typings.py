import hashlib
from enum import Enum

from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat


class EncodingType(str, Enum):
    PEM = "pem"
    DER = "der"
    OPENSSH = "openssh"
    RAW = "raw"
    X962 = "x962"
    SMIME = "smime"


class PrivateFormatType(str, Enum):
    PKCS8 = "pkcs8"
    PKCS12 = "pkcs12"
    TRADITIONAL = "traditional"
    RAW = "raw"


ENCODINGS: dict[str, Encoding] = {
    "pem": Encoding.PEM,
    "der": Encoding.DER,
    "openssh": Encoding.OpenSSH,
    "raw": Encoding.Raw,
    "x962": Encoding.X962,
    "smime": Encoding.SMIME,
}

PRIVATE_FORMATS: dict[str, PrivateFormat] = {
    "pkcs8": PrivateFormat.PKCS8,
    "pkcs12": PrivateFormat.PKCS12,
    "traditional": PrivateFormat.TraditionalOpenSSL,
    "raw": PrivateFormat.Raw
}


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
