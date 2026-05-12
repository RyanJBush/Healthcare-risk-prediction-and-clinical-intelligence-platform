#!/usr/bin/env bash
set -euo pipefail

API_BASE="${API_BASE:-http://localhost:8000}"
ADMIN_USER="${ADMIN_USER:-admin}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-admin123}"
SEED_COUNT="${SEED_COUNT:-20}"
SEED_VALUE="${SEED_VALUE:-13}"
TARGET_TYPE="${TARGET_TYPE:-readmission}"

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required." >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "Error: python is required for JSON parsing." >&2
  exit 1
fi

echo "[1/4] Logging in as ${ADMIN_USER}..."
LOGIN_PAYLOAD=$(printf '{"username":"%s","password":"%s"}' "$ADMIN_USER" "$ADMIN_PASSWORD")
TOKEN=$(curl -sS -X POST "${API_BASE}/auth/login" -H 'Content-Type: application/json' -d "$LOGIN_PAYLOAD" | python -c 'import json,sys; print(json.load(sys.stdin).get("access_token",""))')

if [[ -z "$TOKEN" ]]; then
  echo "Error: could not obtain access token. Is backend running?" >&2
  exit 1
fi

echo "[2/4] Seeding a compact synthetic cohort (count=${SEED_COUNT}, seed=${SEED_VALUE})..."
SEED_PAYLOAD=$(printf '{"count":%s,"seed":%s}' "$SEED_COUNT" "$SEED_VALUE")
curl -sS -X POST "${API_BASE}/api/demo/load-seed" -H "Authorization: Bearer ${TOKEN}" -H 'Content-Type: application/json' -d "$SEED_PAYLOAD" >/dev/null

echo "[3/4] Creating training run for target_type=${TARGET_TYPE}..."
TRAIN_PAYLOAD=$(printf '{"target_type":"%s"}' "$TARGET_TYPE")
TRAIN_RESPONSE=$(curl -sS -X POST "${API_BASE}/api/training/runs" -H "Authorization: Bearer ${TOKEN}" -H 'Content-Type: application/json' -d "$TRAIN_PAYLOAD")

RUN_ID=$(printf '%s' "$TRAIN_RESPONSE" | python -c 'import json,sys; print(json.load(sys.stdin).get("id",""))')
if [[ -z "$RUN_ID" ]]; then
  echo "Error: training run was not created." >&2
  printf '%s\n' "$TRAIN_RESPONSE"
  exit 1
fi

echo "[4/4] Training run created. Fetching run details..."
curl -sS "${API_BASE}/api/training/runs/${RUN_ID}" -H "Authorization: Bearer ${TOKEN}" | python -m json.tool

echo "Small synthetic training workflow complete. Not for clinical use."
