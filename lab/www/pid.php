<?php
declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');
header('X-Worker-Pid: ' . (string) getmypid());
header('X-PHP-Sapi: ' . PHP_SAPI);
header('X-PHP-Version: ' . PHP_VERSION);

echo 'pid=' . getmypid() . "\n";
echo 'sapi=' . PHP_SAPI . "\n";
echo 'version=' . PHP_VERSION . "\n";
echo 'fatal_error_backtraces=' . (string) ini_get('fatal_error_backtraces') . "\n";
echo 'ok' . "\n";
