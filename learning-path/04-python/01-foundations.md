# Foundations

## Why Python in DevOps

- Readable glue for REST and CLIs
- Available on CI images and bastions
- boto3, kubernetes, python-gitlab, Jenkins API
- pytest is the quality bar

Not for: kernel modules, ultra-hot data paths (maybe Go/Rust), or secret storage.

## Runtime hygiene

```text
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
python -m pip install -U pip
```

Pin deps in `requirements.txt` with hashes when you can. Do not `sudo pip install` on a shared host.

## Style that survives review

- `pathlib` over string paths
- type hints on public functions
- `logging` not `print` in anything scheduled
- `if __name__ == "__main__"`
- Catch specific exceptions; print `type(exc).__name__` not secrets in `str(exc)` if it might contain URLs with tokens

## Packaging

A folder with `__init__.py` or a `src/` layout beats 40 unrelated scripts in `$HOME/bin`. Entry points (`python -m mymod`) match how we run the banking agent in this repo.
