#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-cve-2026-109619}"
export PYTHONUNBUFFERED=1

LABEL="CVE-2026-109619"
WITNESS="CVE-2026-109619-UAF-WITNESS"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  down
  exit 1
}

echo "== docker compose down (clean) =="
down

for img in php:8.5.11-apache php:8.5.12-apache; do
  if ! docker image inspect "${img}" >/dev/null 2>&1; then
    echo "== docker pull ${img} =="
    docker pull "${img}" || fail_setup "image-pull-failed:${img}"
  fi
done

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 5); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 8
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait for HTTP 127.0.0.1:18222 and 18223 /pid.php =="
ok=0
for i in $(seq 1 90); do
  if python3 - <<'PY'
import urllib.request
for port in (18222, 18223):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/pid.php", timeout=2) as resp:
        body = resp.read().decode("utf-8", "replace")
        if "ok" not in body or "apache2handler" not in body:
            raise SystemExit(1)
PY
  then
    ok=1
    echo "http-ready attempt=${i}"
    break
  fi
  echo "http-wait attempt=${i}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  fail_setup "http-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

down
exit "${rc}"
