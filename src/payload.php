<?php

/**
 * evil-package DEMO sample (PHP branch).
 *
 * An intentionally SAFE, clearly-labeled demonstration of what a Composer
 * payload looks like. Composer executes no package PHP at install time; this
 * file is a `files` autoload entry, so it runs when the application's
 * vendor/autoload.php is loaded — at boot or in the test suite — which is
 * where the sniff.py sensors see it (the smoke check, not detonation).
 *
 * SAFETY GATE: the payload fires ONLY when CUJO_SANDBOX is set, which the
 * sandbox harness does. A normal `composer install` and boot by anyone else
 * is completely inert.
 */

declare(strict_types=1);

(static function (): void {
    if ((string) getenv('CUJO_SANDBOX') === '') {
        return;
    }

    try {
        fwrite(STDERR, "[evil-package DEMO] Running harmless autoload-time demo payload (supply-chain sandbox demonstration). This payload is SAFE and clearly labeled; it never exfiltrates data and never fails.\n");
    } catch (\Throwable) {
    }

    $home = getenv('HOME') ?: '/root';

    // DEMO step 1: canary egress through the sandbox's logging proxy. curl
    // honours HTTP(S)_PROXY, so the proxy records the unknown host. The
    // .example TLD is unroutable by design; the attempt itself is the signal.
    try {
        shell_exec('curl -sS -m 2 http://canary.cujo-demo.example/ 2>/dev/null');
    } catch (\Throwable) {
    }

    // DEMO step 2: read of ~/.aws/credentials if it exists. The bytes are
    // read and discarded; nothing is done with the contents.
    try {
        $creds = $home . '/.aws/credentials';
        if (is_file($creds)) {
            file_get_contents($creds);
        }
    } catch (\Throwable) {
    }

    // DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
    try {
        file_put_contents(
            $home . '/.cujo-demo-dropper.txt',
            "This file was written by the evil-package DEMO sample at autoload time. It is harmless.\n"
        );
    } catch (\Throwable) {
    }
})();
