//! evil-package DEMO payload for Cargo.
//!
//! Same contract as setup.py: completely inert unless CUJO_SANDBOX is set.
//! Cargo executes a dependency's build script during `cargo build` /
//! `cargo test`, so build.rs is the first point where dependency code runs
//! in this ecosystem. Every action is harmless, observable, and wrapped so
//! the build NEVER fails.

fn main() {
    if std::env::var("CUJO_SANDBOX").is_err() {
        return;
    }

    // DEMO step 1: benign canary egress attempt to an unroutable RFC 5737
    // TEST-NET-3 IP literal. TCP connect only, no data sent, 2s timeout.
    let addr: std::net::SocketAddr = match "203.0.113.10:443".parse() {
        Ok(addr) => addr,
        Err(_) => return,
    };
    let _ = std::net::TcpStream::connect_timeout(&addr, std::time::Duration::from_secs(2));

    // DEMO step 2: read-and-discard of ~/.aws/credentials if it exists.
    if let Ok(home) = std::env::var("HOME") {
        let creds = std::path::Path::new(&home).join(".aws").join("credentials");
        let _ = std::fs::read(creds);
    }

    // DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
    if let Ok(home) = std::env::var("HOME") {
        let marker = std::path::Path::new(&home).join(".cujo-demo-dropper.txt");
        let _ = std::fs::write(
            marker,
            "This file was written by the evil-package DEMO sample at install time. It is harmless.\n",
        );
    }
}
