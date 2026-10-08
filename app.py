import sys
from pathlib import Path

import typer
from cryptography.hazmat.primitives.serialization import NoEncryption

from modules import *
from modules import hash as _hash
from modules import rsa
from modules.typings import (
    ENCODINGS,
    PRIVATE_FORMATS,
    EncodingType,
    HashAlgorithm,
    PrivateFormatType,
)

app = typer.Typer(help="py-crypto: hashing and RSA encryption from the command line.")
hashing = typer.Typer()
rsa_encryption = typer.Typer()

app.add_typer(hashing, name="hashing")
app.add_typer(rsa_encryption, name="rsa")

@hashing.callback()
def hashing_main():
    """Hash text or files, and compare hashes.

        Supports md5, sha1, sha256 (default), sha512, blake2b and blake2s.
        """

@hashing.command()
def hash(
    text: str = typer.Argument(None, help="Text to hash."),
    file: Path | None = typer.Option(None, "--file", "-f", help="File to hash."),
    algorithm: HashAlgorithm = typer.Option(
            HashAlgorithm.SHA256, help="Hash algorithm to use."
        )
    ):
    """Hash text or a file and print the hex digest.

    Give either TEXT or --file, not both.

    Example: hashing hash "hello world" --algorithm sha512
    """

    if text and file is not None:
        raise typer.BadParameter("Use either text or --file, not both.")

    if file is not None:
        if not file.exists():
            raise typer.BadParameter(f"File does not exist: {file}")

        if not file.is_file():
            raise typer.BadParameter(f"Not a file: {file}")

        result = _hash.file(file, algorithm)

    elif text:
        result = _hash.text(text, algorithm)

    else:
        raise typer.BadParameter("Provide text or use --file.")

    typer.echo(result)

@hashing.command()
def compare(
    input_hash: str | None = typer.Argument(None, help="Text or file path to hash. If it is an existing file, its contents are hashed; otherwise the text is hashed.",),
    known_hash: str | None = typer.Argument(None, help="Expected hex digest, or a second file path to compare the first file against."),
    algorithm: HashAlgorithm = typer.Option(
           HashAlgorithm.SHA256, help="Hash algorithm to use for both sides.")
    ):
    """Check a text or file against a known hash, or two files against each other.

        The first argument is the thing to hash and the second is what to compare it to:
        file + file hashes both and compares them, file + digest hashes the file and
        compares it to the digest, text + digest hashes the text and compares it.

        Prints a result panel. Exits with a non-zero status on a mismatch.
    """

    comp_text = ""
    text = "[green]Text[/green]"
    file = "[blue]File[/blue]"

    if input_hash is None:
        raise typer.BadParameter("Provide a string or file path.")

    if known_hash is None:
        raise typer.BadParameter("Provide a string to compare.")

    path = Path(input_hash)
    path2 = Path(known_hash)

    if path.is_file() and path2.is_file():
        comp_text = f"{file} v.s {file}"
        res = _hash.file_compare(path, path2, algorithm)
    elif path.is_file():
        comp_text = f"{file} v.s {text}"
        res = _hash.file_compare(path, known_hash, algorithm)
    else:
        comp_text = f"{text} v.s {text}"
        res = _hash.text_compare(input_hash, known_hash, algorithm)

    if res:
        success(
            Algorithm=algorithm.name,
            Type=f"{comp_text}",
            Verdict="Match"
        )
    else:
        fail(
            Algorithm=algorithm.name,
            Type=f"{comp_text}",
            Verdict="MisMatch"
        )
        sys.exit(-1)

@rsa_encryption.callback()
def rsa_encryption_main():
    """Generate RSA keys and encrypt messages.

    Keys are read from and written to the current directory as private.pem
    and public.pem. Typical flow: new-private, then new-pub, then encrypt.
    """


@rsa_encryption.command()
def encrypt(
    message: str = typer.Argument(None, help="Plain text message to encrypt (short messages only)."),
    path: str = typer.Argument(None, help="Path to the PEM public key file, for example public.pem.")
    ):
    """Encrypt a message with an RSA public key and print the hex ciphertext.

        Uses RSA-OAEP with SHA-256. A 3072-bit key can encrypt at most 318 bytes.
    """
    if not message or not path:
        raise typer.BadParameter("Please enter a message adn the path to the pem file.")

    pem_path = Path(path)
    ret = rsa.encrypt_message(
        pem_path,
        message
    )

    print(ret)

@rsa_encryption.command()
def new_pub(
    path: str = typer.Argument(None, help="Path to a PEM private key file, for example private.pem.")
    ):
    """
        Create public.pem in the current directory from a private key.

        Overwrites any existing public.pem. The private key must be an
        unencrypted PEM file.
    """

    private_path = Path(path)
    if not private_path.is_file():
        raise typer.BadParameter("Argument given is not a valid path")

    rsa.create_public_key(private_path)

@rsa_encryption.command()
def new_private(
    public_exponent: int = typer.Option(
               65537, help="RSA public exponent. 65537 is the standard choice."
           ),
    key_size: int = typer.Option(3072, help="Key length in bits."),
           encoding: EncodingType = typer.Option(
               EncodingType.PEM,
               help="Key file encoding. Only pem and der work for RSA keys.",
           ),
    private_format: PrivateFormatType = typer.Option(
               PrivateFormatType.PKCS8,
               help="Private key format. Only pkcs8 and traditional work for RSA keys.",)
    ):
    """Generate a new RSA private key and save it as private.pem.

    The key is written unencrypted to the current directory and overwrites any
        existing private.pem. Use pem encoding if you want to run new-pub on it.
    """

    encoding_type = ENCODINGS[encoding.value]
    format_type = PRIVATE_FORMATS[private_format.value]

    rsa.create_private_key(
        public_exponent,
        key_size,
        encoding_type,
        format_type,
        NoEncryption(),
    )

if __name__ == "__main__":
    app()
