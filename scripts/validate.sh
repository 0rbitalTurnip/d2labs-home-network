#!/usr/bin/env bash
set -euo pipefail

echo "d2lab local validation script"

REQUIRED_FILES=(
  "docs/configs/opnsense-vlans.example.xml"
  "docs/configs/mhv-interfaces.example"
  "docs/configs/inventory.csv"
  "examples/gluetun/docker-compose.yml"
  "examples/gluetun/.env.example"
  "scripts/build_pdf.py"
  "requirements.txt"
)

missing=0
for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -e "$f" ]; then
    echo "MISSING: $f"
    missing=1
  fi
done

if [ $missing -eq 1 ]; then
  echo "One or more required files are missing. See messages above." >&2
  exit 2
fi

echo "Required files present. Checking Python dependencies..."
python3 - <<'PY'
import sys
missing=[]
for m in ("reportlab","pypdf"):
    try:
        __import__(m)
    except Exception:
        missing.append(m)
if missing:
    print("Missing python packages:", missing)
    sys.exit(3)
print("Python deps OK")
PY

echo "Building PDF (this will write to ./diagrams/)"
python3 scripts/build_pdf.py --out ./diagrams/d2lab-network-overview.pdf

echo "Linting JSON files..."
find . -name '*.json' -not -path './.git/*' -print0 | xargs -0 -n1 python3 -m json.tool || echo "JSON lint errors detected"

if command -v yamllint >/dev/null 2>&1; then
  echo "Running yamllint..."
  yamllint . || echo "yamllint reported issues"
else
  echo "yamllint not installed; skipping YAML lint (install with 'pip install yamllint')"
fi

echo "Validation complete."
