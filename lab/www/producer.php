<?php
declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');
header('X-Worker-Pid: ' . (string) getmypid());

function producer_leaf(string $blob): void
{
    trigger_error('CVE-2026-109619 producer fatal blob=' . $blob, E_USER_ERROR);
}

function producer_frame(int $depth, string $blob): void
{
    if ($depth <= 0) {
        producer_leaf($blob);
        return;
    }
    producer_frame($depth - 1, $blob);
}

producer_frame(12, str_repeat('UAF', 1024));
