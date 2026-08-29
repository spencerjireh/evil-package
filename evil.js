// evil-package DEMO sample (npm branch).
//
// An intentionally SAFE, clearly-labeled demonstration of what an npm
// install-time payload looks like. `postinstall` runs this file when the
// package is installed as a dependency. Every action is harmless, observable,
// and wrapped so the install NEVER fails.
//
// SAFETY GATE: the payload fires ONLY when CUJO_SANDBOX is set, which the
// sniff.py detonation harness does. A normal `npm install` by anyone else is
// completely inert.

const os = require("os");
const fs = require("fs");
const path = require("path");
const { execFile } = require("child_process");

const BANNER =
  "[evil-package DEMO] Running harmless install-time demo payload " +
  "(supply-chain sandbox demonstration). This payload is SAFE and clearly " +
  "labeled; it never exfiltrates data and never fails the install.";

function payload() {
  console.log(BANNER);

  // DEMO step 1: canary egress through the sandbox's logging proxy. curl
  // honours HTTP(S)_PROXY, so the proxy records the unknown host. The .example
  // TLD is unroutable by design; the attempt itself is the signal. Node's
  // fetch ignores proxy variables, which is why this shells out to curl.
  try {
    execFile("curl", ["-sS", "-m", "2", "http://canary.cujo-demo.example/"], () => {});
  } catch {
    /* never fail the install */
  }

  // DEMO step 2: read of ~/.aws/credentials if it exists. The bytes are read
  // and discarded; nothing is done with the contents.
  try {
    const creds = path.join(os.homedir(), ".aws", "credentials");
    if (fs.existsSync(creds)) fs.readFileSync(creds);
  } catch {
    /* never fail the install */
  }

  // DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
  try {
    fs.writeFileSync(
      path.join(os.homedir(), ".cujo-demo-dropper.txt"),
      "This file was written by the evil-package DEMO sample at install " +
        "time. It is harmless.\n"
    );
  } catch {
    /* never fail the install */
  }
}

if (process.env.CUJO_SANDBOX) {
  try {
    payload();
  } catch {
    /* never fail the install */
  }
}
