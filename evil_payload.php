<?php
/**
 * evil-package DEMO payload for Composer.
 *
 * Same contract as setup.py: completely inert unless CUJO_SANDBOX is set.
 * The autoload.files entry makes this file run at require-time of the
 * generated autoloader (require vendor/autoload.php), which is where
 * dependency code first executes in this ecosystem. Every action is
 * harmless, observable, and suppressed so nothing ever fails.
 */

if (getenv('CUJO_SANDBOX') === false) {
    return;
}

// DEMO step 1: benign canary egress attempt to an unroutable RFC 5737
// TEST-NET-3 IP literal. TCP connect only, no data sent, 2s timeout.
@stream_socket_client(
    'tcp://203.0.113.10:443',
    $errno,
    $errstr,
    2.0
);

// DEMO step 2: read-and-discard of ~/.aws/credentials if it exists.
$home = getenv('HOME');
if ($home !== false) {
    $creds = $home . '/.aws/credentials';
    if (@is_file($creds)) {
        @file_get_contents($creds);
    }
}

// DEMO step 3: harmless, clearly-labeled dropper marker in $HOME.
if ($home !== false) {
    @file_put_contents(
        $home . '/.cujo-demo-dropper.txt',
        "This file was written by the evil-package DEMO sample at install time. It is harmless.\n"
    );
}
