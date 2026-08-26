"""setup.py for the evil-package DEMO sample.

This package is an intentionally SAFE, clearly-labeled demonstration of what an
install-time supply-chain payload looks like. Every action below is harmless,
observable, and wrapped so the install NEVER fails. See README.md before doing
anything with this package.

WHERE THE PAYLOAD RUNS
----------------------
The payload runs at the top level of this setup.py, which is executed by the
build/install tooling itself: pip's PEP 517 build runs setup.py in a subprocess
to produce the wheel, and `python setup.py install` runs it too. So a normal
`pip install git+https://.../evil-package` detonates it -- which is how the demo
PR delivers it. Importing the installed `evil_package` module never runs any of
this; setup.py is not imported by the package, only executed at build/install.
"""

import os
import socket

from setuptools import setup

DEMO_BANNER = (
    "[evil-package DEMO] Running harmless install-time demo payload "
    "(supply-chain sandbox demonstration). This payload is SAFE and clearly "
    "labeled; it never exfiltrates data and never fails the install."
)


def _run_demo_payload():
    """Three observable-but-harmless actions, each isolated so nothing fails."""
    print(DEMO_BANNER)

    # DEMO step 1: benign canary egress attempt. Connects to an IP literal in
    # the RFC 5737 TEST-NET-3 documentation range (203.0.113.0/24), which is
    # guaranteed unroutable. Using an IP literal skips DNS, so this always
    # issues a real socket.connect (which the audit-hook egress sensor records)
    # that then times out. TCP connect only, no data is sent, all errors
    # swallowed. Registers as egress to a non-index host.
    try:
        conn = socket.create_connection(("203.0.113.10", 443), timeout=2)
        conn.close()
    except Exception:
        pass

    # DEMO step 2: audit-hook-visible read of ~/.aws/credentials if it exists.
    # The bytes are read and discarded; nothing is done with the contents.
    # Skipped quietly if the file is absent.
    try:
        aws_creds_path = os.path.expanduser("~/.aws/credentials")
        if os.path.exists(aws_creds_path):
            with open(aws_creds_path, "rb") as fh:
                fh.read()
    except Exception:
        pass

    # DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
    try:
        marker_path = os.path.expanduser("~/.cujo-demo-dropper.txt")
        with open(marker_path, "w") as fh:
            fh.write(
                "This file was written by the evil-package DEMO sample "
                "at install time. It is harmless.\n"
            )
    except Exception:
        pass


# Fire the payload when this setup.py is executed by the build/install tooling.
# The whole call is guarded so a failure here can never break the install.
try:
    _run_demo_payload()
except Exception:
    pass


setup(
    name="evil-package",
    version="0.0.1",
    description=(
        "Intentionally harmless DEMO sample for a dependency-sandbox security "
        "tool. Never install outside a sandbox. Not published to PyPI."
    ),
    packages=["evil_package"],
)
