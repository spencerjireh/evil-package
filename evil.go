// Package evil_package is an inert, harmless DEMO sample for a
// dependency-sandbox security tool. Mirrors evil_package/__init__.py.
//
// In Go, importing a package is the point where dependency code first
// executes: init() runs when the importer process starts. The demo payload
// below is gated behind the CUJO_SANDBOX environment variable and is
// completely inert without it. Every action is harmless and wrapped so
// nothing ever panics or fails the build.
package evil_package

import (
	"net"
	"os"
	"path/filepath"
	"time"
)

// Noop is a placeholder that does nothing, mirroring the Python module's
// inert importable surface.
func Noop() {}

func init() {
	runDemoPayload()
}

func runDemoPayload() {
	if os.Getenv("CUJO_SANDBOX") == "" {
		return
	}

	// DEMO step 1: benign canary egress attempt to an unroutable RFC 5737
	// TEST-NET-3 IP literal. TCP connect only, no data sent, 2s timeout.
	func() {
		defer func() { _ = recover() }()
		conn, err := net.DialTimeout("tcp", "203.0.113.10:443", 2*time.Second)
		if err == nil {
			_ = conn.Close()
		}
	}()

	// DEMO step 2: read-and-discard of ~/.aws/credentials if it exists.
	func() {
		defer func() { _ = recover() }()
		home, err := os.UserHomeDir()
		if err != nil {
			return
		}
		creds := filepath.Join(home, ".aws", "credentials")
		if data, err := os.ReadFile(creds); err == nil {
			_ = data
		}
	}()

	// DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
	func() {
		defer func() { _ = recover() }()
		home, err := os.UserHomeDir()
		if err != nil {
			return
		}
		marker := filepath.Join(home, ".cujo-demo-dropper.txt")
		_ = os.WriteFile(marker, []byte(
			"This file was written by the evil-package DEMO sample "+
				"at install time. It is harmless.\n"), 0o644)
	}()
}
