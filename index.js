"use strict";

/**
 * Inert importable entry point, mirroring evil_package/__init__.py.
 * Requiring this module does nothing and triggers nothing; the demo
 * payload lives only in evil_payload.js behind the preinstall script.
 */

function noop() {
  return null;
}

module.exports = {
  noop: noop,
};
