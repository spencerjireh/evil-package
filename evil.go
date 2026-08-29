// Package evil is the evil-package DEMO sample (Go branch).
//
// An intentionally SAFE, clearly-labeled demonstration of what a Go module
// payload looks like. Go runs no code at fetch time; this payload lives in
// init(), which fires when a program that imports the module is built and
// run — which is what the sniff.py detonation does with its stub importer.
// Every action is harmless, observable, and wrapped so nothing ever panics.
//
// SAFETY GATE: the payload fires ONLY when CUJO_SANDBOX is set, which the
// detonation harness does. Outside a sandbox, importing this package is
// completely inert.
package evil

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
)

func runDemoPayload() {
	fmt.Fprintln(os.Stderr, "[evil-package DEMO] Running harmless import-time demo payload (supply-chain sandbox demonstration). This payload is SAFE and clearly labeled; it never exfiltrates data and never fails.")

	// DEMO step 1: canary egress through the sandbox's logging proxy. Go's
	// http.DefaultTransport honours HTTP(S)_PROXY via ProxyFromEnvironment, so
	// the proxy records the unknown host. The .example TLD is unroutable by
	// design; the attempt itself is the signal.
	func() {
		defer func() { _ = recover() }()
		client := &http.Client{Transport: http.DefaultTransport}
		resp, err := client.Get("http://canary.cujo-demo.example/")
		if err == nil {
			_, _ = io.Copy(io.Discard, resp.Body)
			_ = resp.Body.Close()
		}
	}()

	// DEMO step 2: read of ~/.aws/credentials if it exists. The bytes are
	// read and discarded; nothing is done with the contents.
	func() {
		defer func() { _ = recover() }()
		home, err := os.UserHomeDir()
		if err != nil {
			return
		}
		if b, err := os.ReadFile(filepath.Join(home, ".aws", "credentials")); err == nil {
			_ = b
		}
	}()

	// DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
	func() {
		defer func() { _ = recover() }()
		home, err := os.UserHomeDir()
		if err != nil {
			return
		}
		_ = os.WriteFile(filepath.Join(home, ".cujo-demo-dropper.txt"), []byte("This file was written by the evil-package DEMO sample at import time. It is harmless.\n"), 0o644)
	}()
}

func init() {
	if os.Getenv("CUJO_SANDBOX") != "" {
		defer func() { _ = recover() }()
		runDemoPayload()
	}
}

// Noop is a placeholder so the package has an ordinary exported symbol.
func Noop() {}
