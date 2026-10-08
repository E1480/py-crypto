from pathlib import Path
from typing import cast

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    KeySerializationEncryption,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
    load_pem_public_key,
)


def create_private_key(
    public_exponent: int = 65537,
    key_size: int = 3072,
    encoding: Encoding = Encoding.PEM,
    format: PrivateFormat = PrivateFormat.PKCS8,
    encryption_algorithm: KeySerializationEncryption = NoEncryption()
    ):
    key = rsa.generate_private_key(public_exponent, key_size)

    with open("private.pem", 'wb') as kf:
        _ = kf.write(key.private_bytes(encoding, format, encryption_algorithm))

def create_public_key(private_key: Path):

    if not private_key.is_file():
        raise ValueError("Path provided is not a file!")

    with private_key.open("rb") as pk:
        key = load_pem_private_key(pk.read(), None)

    k = cast(RSAPublicKey,key.public_key())
    with open("public.pem", 'wb') as f:
        _ = f.write(k.public_bytes(encoding=Encoding.PEM, format=PublicFormat.PKCS1))

def create_cipher(public_key: Path):

    if not public_key.is_file():
        raise ValueError("Path provided is not a file!")

    with public_key.open("rb") as pk:
        key = load_pem_public_key(pk.read())

    return cast(RSAPublicKey, key)

def encrypt_message(key_file: Path, message: str):
    cipher = create_cipher(key_file)

    encrypted = cipher.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ),
    )

    return encrypted.hex()

# def _generate():

#     messsage = b"test"
#     private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
#     public_key = private_key.public_key()

#     cipher = public_key.encrypt(
#         messsage,
#         padding.OAEP(
#             mgf=padding.MGF1(hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )

#     print(f"Encrypted: {cipher}")

#     plain_text = private_key.decrypt(
#             cipher,
#             padding.OAEP(
#             mgf=padding.MGF1(hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )

#     print(f"Decrypted: {plain_text}")
