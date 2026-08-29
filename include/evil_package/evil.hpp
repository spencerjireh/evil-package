// evil-package DEMO header for Conan/C++ consumers.
//
// This header is inert, mirroring evil_package/__init__.py: including it
// does nothing and triggers nothing. For this ecosystem the demo payload
// lives in the conanfile.py recipe, which Conan executes at create/build
// time behind the CUJO_SANDBOX gate.

#pragma once

namespace evil_package {

// No-op placeholder. Does nothing.
inline void noop() {}

}  // namespace evil_package
