# py-crypto

A small command-line toolkit for everyday cryptography tasks, built with
[Typer](https://typer.tiangolo.com/) and [Rich](https://github.com/Textualize/rich):

- **Hashing**: hash text or files, and compare them against a known hash or another file.
- **RSA**: generate key pairs and encrypt messages with a public key.


> [!WARNING] 
> This is a learning/utility project. It has not been security audited, and
> private keys are written to disk **unencrypted**. See [Known issues](#known-issues).

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended), or pip

## Installation

```bash
git clone https://github.com/E1480/py-crypto
cd py-crypto
uv sync
```

Then run the CLI with:

```bash
uv run python app.py --help
```

## Usage

The CLI has two command groups: `hashing` and `rsa`.

Every command has built-in help describing its arguments and options:

```bash
uv run python app.py --help                  # list the command groups
uv run python app.py hashing --help          # list the hashing commands
uv run python app.py hashing compare --help  # help for a single command
```

### Hashing

Supported algorithms (`--algorithm`): `md5`, `sha1`, `sha256` (default),
`sha512`, `blake2b`, `blake2s`.

**Hash text**

```bash
uv run python app.py hashing hash "hello world"
uv run python app.py hashing hash "hello world" --algorithm sha512
```

**Hash a file**

```bash
uv run python app.py hashing hash --file ./document.pdf
```

Provide either text or `--file`, not both.

**Compare against a known hash**

`compare` takes the thing to hash first and what to compare it to second:

| First argument | Second argument | What happens                                       |
| -------------- | --------------- | -------------------------------------------------- |
| file path      | file path       | Both files are hashed and compared                 |
| file path      | hex digest      | The file is hashed and compared to the digest      |
| text           | hex digest      | The text is hashed and compared to the digest      |

The order matters. Putting the digest first and a file second is treated as
text vs text and reports a mismatch.

```bash
uv run python app.py hashing compare ./download.iso <expected-sha256-digest>
```

Results are shown in a Rich panel. On a mismatch the process exits with a
non-zero status, so it can be used in scripts.

### RSA

Keys are read from and written to the **current working directory**. `*.pem`
files are git-ignored.

**1. Generate a private key** (writes `private.pem`)

```bash
uv run python app.py rsa new-private
uv run python app.py rsa new-private --key-size 4096
```

| Option             | Default | Choices                                           |
| ------------------ | ------- | ------------------------------------------------- |
| `--public-exponent`| 65537   | any int                                           |
| `--key-size`       | 3072    | any valid RSA size in bits                        |
| `--encoding`       | `pem`   | `pem`, `der`, `openssh`, `raw`, `x962`, `smime`   |
| `--private-format` | `pkcs8` | `pkcs8`, `pkcs12`, `traditional`, `raw`           |

For RSA keys only `pem` or `der` encoding combined with `pkcs8` or
`traditional` format works. Every other combination fails with a `ValueError`
(see [Known issues](#known-issues)). `new-pub` and `encrypt` read PEM files,
so use the default `pem` encoding if you want to continue with those commands.

**2. Derive the public key** (writes `public.pem`)

```bash
uv run python app.py rsa new-pub private.pem
```

**3. Encrypt a message**

```bash
uv run python app.py rsa encrypt "secret message" public.pem
```

Prints the ciphertext as a hex string. Encryption uses RSA-OAEP with SHA-256.
RSA can only encrypt short messages (at most 318 bytes for a 3072-bit key).

> [!NOTE]
> There is currently no `decrypt` command.   :)

## Project structure

```
py-crypto/
├── app.py              # CLI entry point (Typer app: `hashing` and `rsa` groups)
├── modules/
│   ├── __init__.py     # Rich console output helpers: success() / fail()
│   ├── hash.py         # Text/file hashing and comparison functions
│   ├── rsa.py          # RSA key generation and encryption
│   └── typings.py      # Hash/encoding/format enums and their lookup tables
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions
└── .python-version     # Python version used for development (3.13)
```

## Dependencies

| Package        | Purpose                                         |
| -------------- | ----------------------------------------------- |
| `typer`        | CLI framework and `--help` output               |
| `rich`         | Formatted terminal output                       |
| `cryptography` | RSA key generation, serialization, and OAEP     |

## Known issues

1. **Private keys are unencrypted.** `new-private` always uses `NoEncryption()`,
   so `private.pem` is stored in plain text. Protect it accordingly and never commit it.
   
2. **Output files overwrite silently.** `private.pem` and `public.pem` are
   always written to the current directory and replace existing files.
   
3. **Unsupported key options leave an empty `private.pem`.** The file is opened
   before the key is serialized, so an unsupported `--encoding` /
   `--private-format` combination crashes with a `ValueError` after
   truncating any existing `private.pem`. Back up your key first.
   
4. **`rsa new-pub` without a path crashes** with a `TypeError` instead of
   showing a friendly error.
   
5. **Repeated panel rows.** `success()`/`fail()` share one module-level table
   that is never cleared; fine for a single CLI run, but rows would pile up if
   called multiple times in one process.
   
6. **`md5` and `sha1`** are included but are not collision-resistant. Don't rely
   on them for security.

## License

This project is licensed under the [MIT License](LICENSE).
