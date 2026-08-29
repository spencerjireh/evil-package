# evil-package (Rust branch `rust`)

> SAFETY: deliberate, harmless demo sample. The payload is gated behind the
> `CUJO_SANDBOX` environment variable, so a normal `pip install` is completely
> inert. See [SECURITY.md](SECURITY.md).

**This is a deliberate, harmless DEMO sample for a security sandbox.**

This package exists only to demonstrate, in a controlled and observable
way, what an install-time supply-chain payload looks like when a
dependency-sandbox tool evaluates it. It is a demonstration artifact,
not real software.

## Ground rules

- This package is **never published to PyPI**.
- It is pulled **only via a `git+https` line in a demo PR**, for example
  (placeholder host): `evil-package @ git+https://<demo-git-host>/<org>/evil-package.git`
- **Never install this package outside a sandbox** (an isolated VM,
  container, or other throwaway environment). Even though the payload is
  harmless by construction, treat it as untrusted.
- Do not fork this into anything that carries out real actions.

## What the payload does

The payload runs at the top level of `setup.py`, which the build tooling
executes: pip's PEP 517 build runs `setup.py` in a subprocess, and
`python setup.py install` runs it too. So a normal
`pip install git+https://.../evil-package` fires it. **Merely importing
the `evil_package` module does NOT trigger anything**; the importable
module is inert.

At install time, the payload performs three observable-but-harmless
actions. Each is wrapped in its own `try/except` so the install NEVER
fails and nothing harmful happens:

1. Attempts a TCP connection to `203.0.113.10:443` with a ~2 second
   timeout. `203.0.113.10` is a benign, unroutable IP literal from the
   RFC 5737 TEST-NET-3 documentation range; using an IP literal skips DNS
   so the connect attempt always registers as egress to a non-index host.
   No data is sent. All errors are swallowed.
2. If `~/.aws/credentials` exists, opens it and reads its bytes so a
   Python audit hook observing `open` events records the read. The
   contents are read and discarded; nothing is done with them. If the
   file does not exist, this step is skipped quietly.
3. Writes a clearly-labeled harmless marker file, `~/.cujo-demo-dropper.txt`,
   containing exactly:

   > This file was written by the evil-package DEMO sample at install
   > time. It is harmless.

## Behavior notes

- The payload runs at `setup.py` execution time, so it fires on the
  normal `pip install` path (pip executes `setup.py` in its build
  subprocess under PEP 517) as well as on `python setup.py install` -- but
  only when the `CUJO_SANDBOX` environment variable is set.
- The payload is **gated behind `CUJO_SANDBOX`**. The sniff.py detonation
  harness sets `CUJO_SANDBOX=1` before installing, so the demo fires. Any
  normal `pip install` without that variable is completely inert: no network,
  no file reads, no writes.
- Everything the payload does is visible in `setup.py`. There is no
  obfuscation, no network data exfiltration, and no destructive action.

## Repo layout

- `setup.py` — package metadata plus the top-level harmless demo payload
  that runs when the build/install tooling executes `setup.py`.
- `evil_package/__init__.py` — inert importable module with
  `__version__` and a no-op function.
