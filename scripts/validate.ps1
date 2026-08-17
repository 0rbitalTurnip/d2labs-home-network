<#
Local validation script for d2lab (PowerShell)
Checks required files, Python deps, JSON lint, optional yamllint, and runs the PDF build.
#>
Write-Host "d2lab local validation (PowerShell)"

$required = @(
  'docs/configs/opnsense-vlans.example.xml',
  'docs/configs/mhv-interfaces.example',
  'docs/configs/inventory.csv',
  'examples/gluetun/docker-compose.yml',
  'examples/gluetun/.env.example',
  'scripts/build_pdf.py',
  'requirements.txt'
)

$missing = $false
foreach ($f in $required) {
  if (-not (Test-Path $f)) {
    Write-Host "MISSING: $f" -ForegroundColor Red
    $missing = $true
  }
}
if ($missing) {
  Write-Error "One or more required files are missing. Aborting."
  exit 2
}

Write-Host "Required files present. Checking Python dependencies..."
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "Python not found on PATH"; exit 3 }

$check = @"
import sys
missing=[]
for m in ("reportlab","pypdf"):
    try:
        __import__(m)
    except Exception:
        missing.append(m)
if missing:
    print('MISSING:'+','.join(missing))
    sys.exit(3)
print('PYOK')
"@

$result = & $py.Source -c $check 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) {
  Write-Host $result
  Write-Error "Missing Python packages or other error. Install via 'pip install -r requirements.txt'"
  exit 4
}
Write-Host "Python deps OK"

Write-Host "Building PDF..."
& $py.Source scripts/build_pdf.py --out ./diagrams/d2lab-network-overview.pdf
if ($LASTEXITCODE -ne 0) { Write-Error "PDF build failed"; exit 5 }

Write-Host "Linting JSON files..."
Get-ChildItem -Recurse -Filter '*.json' -ErrorAction SilentlyContinue | ForEach-Object {
  try { python -m json.tool $_.FullName > $null } catch { Write-Host "JSON lint error in $_.FullName" -ForegroundColor Yellow }
}

if (Get-Command yamllint -ErrorAction SilentlyContinue) {
  Write-Host "Running yamllint..."
  yamllint .
} else {
  Write-Host "yamllint not installed; skipping YAML lint (install with 'pip install yamllint')"
}

Write-Host "Validation complete."
