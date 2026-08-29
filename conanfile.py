"""conanfile.py for the evil-package DEMO sample (C++ branch).

An intentionally SAFE, clearly-labeled demonstration of what a Conan recipe
payload looks like. Conan Center ships binaries, so nothing runs for a center
dependency; a recipe from git is executed by `conan create` (or any build from
source), which is what the sniff.py detonation does. The payload below lives
at recipe import time, runs inside conan's Python, and is wrapped so the
recipe NEVER fails.

SAFETY GATE: the payload fires ONLY when CUJO_SANDBOX is set, which the
detonation harness does. A normal `conan create` by anyone else is completely
inert.
"""

import os
import urllib.request

from conan import ConanFile


def _run_demo_payload():
    print(
        "[evil-package DEMO] Running harmless recipe-time demo payload "
        "(supply-chain sandbox demonstration). This payload is SAFE and "
        "clearly labeled; it never exfiltrates data and never fails."
    )

    # DEMO step 1: canary egress through the sandbox's logging proxy.
    # urllib honours HTTP(S)_PROXY by default, so the proxy records the
    # unknown host. The .example TLD is unroutable by design; the attempt
    # itself is the signal.
    try:
        urllib.request.urlopen("http://canary.cujo-demo.example/", timeout=2)
    except Exception:
        pass

    # DEMO step 2: read of ~/.aws/credentials if it exists. The bytes are
    # read and discarded; nothing is done with the contents.
    try:
        creds = os.path.expanduser("~/.aws/credentials")
        if os.path.exists(creds):
            with open(creds, "rb") as fh:
                fh.read()
    except Exception:
        pass

    # DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
    try:
        with open(os.path.expanduser("~/.cujo-demo-dropper.txt"), "w") as fh:
            fh.write(
                "This file was written by the evil-package DEMO sample "
                "at recipe time. It is harmless.\n"
            )
    except Exception:
        pass


if os.environ.get("CUJO_SANDBOX"):
    try:
        _run_demo_payload()
    except Exception:
        pass


class EvilPackageConan(ConanFile):
    name = "evil-package"
    version = "0.0.1"
    description = (
        "Intentionally harmless DEMO sample for a dependency-sandbox "
        "security tool. Never build outside a sandbox."
    )
    license = "MIT"

    def package_id(self):
        # The sample has no source and no artifacts; one id for all.
        self.info.clear()
