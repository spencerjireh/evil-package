# Security notice

**This repository is a deliberate, harmless demonstration sample. It is not real
software and is not malware.**

`evil-package` exists only to show, in a controlled and observable way, what an
install-time supply-chain payload looks like when a dependency-sandbox security
tool evaluates it. It is a test fixture for that tool.

## What it does and does not do

- It is **never published to PyPI**. It is pulled only via a `git+https` line in
  a demo pull request.
- The payload is **gated behind the `CUJO_SANDBOX` environment variable**. A
  normal `pip install` by anyone who does not set that variable is **completely
  inert**: it makes no network connection, reads no files, and writes nothing.
- When the sandbox harness sets `CUJO_SANDBOX`, the payload performs three
  harmless, observable actions: a connection attempt to an unroutable
  documentation IP (`203.0.113.10`, RFC 5737) that **sends no data**; a
  read-and-discard of `~/.aws/credentials` if it exists (contents are never used,
  stored, or transmitted); and a clearly-labeled marker file written to
  `~/.cujo-demo-dropper.txt`.
- There is **no data exfiltration**, no obfuscation, and no destructive action.
  Everything the payload does is visible in `setup.py`.

## Rules

- **Do not install this package outside a sandbox** (an isolated VM, container,
  or other throwaway environment). Treat it as untrusted regardless of the safety
  gate.
- Do not fork or adapt this into anything that carries out real actions.

## Reporting

If you believe this repository is being used improperly, or you have a concern,
open an issue on this repository.
