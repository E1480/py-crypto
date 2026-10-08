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

app = typer.Typer()
hashing = typer.Typer()
rsa_encryption = typer.Typer()

app.add_typer(hashing, name="hashing")
app.add_typer(rsa_encryption, name="rsa")

@hashing.callback()
def hashing_main():
    """ A command to hash files or texts """

@hashing.command()
def hash(
    text: str = typer.Argument(None, help="Text to hash."),
    file: Path | None = typer.Option(None, "--file", "-f", help="File to hash."),
    algorithm: HashAlgorithm = HashAlgorithm.SHA256,
    ):
    """Hash text or a file."""

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
    input_hash: str | None = typer.Argument(None),
    known_hash: str | None = typer.Argument(None),
    algorithm: HashAlgorithm = HashAlgorithm.SHA256,
    ):
    """Compare a file or text hash to a known hash."""

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
    """ Using RSA encryption to encrypt data
        Using pre made public and private keys.
    """


@rsa_encryption.command()
def encrypt(
    message: str = typer.Argument(None),
    path: str = typer.Argument(None)
    ):

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
    path: str = typer.Argument(None)
    ):

        private_path = Path(path)
        if not private_path.is_file():
            raise typer.BadParameter("Argument given is not a valid path")

        rsa.create_public_key(private_path)

@rsa_encryption.command()
def new_private(
        public_exponent: int = 65537,
        key_size: int = 3072,
        encoding: EncodingType = EncodingType.PEM,
        private_format: PrivateFormatType = PrivateFormatType.PKCS8,
    ):

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
