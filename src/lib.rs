//! Inert importable library, mirroring evil_package/__init__.py.
//!
//! Nothing in this crate's library code performs any action; the demo
//! payload lives only in build.rs behind the CUJO_SANDBOX gate.

/// No-op placeholder. Does nothing, returns None.
#[allow(clippy::unused_unit)]
pub fn noop() {}
