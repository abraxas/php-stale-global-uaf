<?php
declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');
header('X-Worker-Pid: ' . (string) getmypid());

echo 'consumer-ok pid=' . getmypid() . "\n";
echo 'sapi=' . PHP_SAPI . "\n";
echo 'version=' . PHP_VERSION . "\n";
