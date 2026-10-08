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
    PKC12 = "pkc12"
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
