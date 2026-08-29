"""Conan recipe for the evil-package DEMO sample.

Same contract as setup.py: completely inert unless CUJO_SANDBOX is set.
Conan executes this recipe during `conan create` and during
`conan install --build`, which is where dependency code first runs in this
ecosystem. The payload below mirrors setup.py exactly; every action is
harmless, observable, and wrapped so the recipe NEVER fails.
"""

import os
import socket

from conan import ConanFile
from conan.tools.files import copy


def _run_demo_payload():
    print(
        "[evil-package DEMO] Running harmless install-time demo payload "
        "(supply-chain sandbox demonstration). This payload is SAFE and clearly "
        "labeled; it never exfiltrates data and never fails the install."
    )

    # DEMO step 1: benign canary egress attempt (unroutable TEST-NET-3).
    try:
        conn = socket.create_connection(("203.0.113.10", 443), timeout=2)
        conn.close()
    except Exception:
        pass

    # DEMO step 2: audit-visible read-and-discard of ~/.aws/credentials.
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


# SAFETY GATE: identical to setup.py. Fires only when CUJO_SANDBOX is set.
if os.environ.get("CUJO_SANDBOX"):
    try:
        _run_demo_payload()
    except Exception:
        pass


class EvilPackageConan(ConanFile):
    name = "evil-package"
    version = "0.1.0"
    description = (
        "Intentionally harmless DEMO sample for a dependency-sandbox security "
        "tool. Never install outside a sandbox. Not published to ConanCenter."
    )
    license = "MIT"
    exports_sources = "include/*"
    no_copy_source = True

    def package(self):
        copy(
            self,
            "*.hpp",
            os.path.join(self.source_folder, "include"),
            os.path.join(self.package_folder, "include"),
        )

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
