# Selenium + Python + GitHub Actions (Minimal)

## Localda ishga tushirish

### Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# GUI bilan ko'rish (HEADLESS=0)
$env:HEADLESS="0"
pytest -v

# Headless test
$env:HEADLESS="1"
pytest -v

### Linux/Mac
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

HEADLESS=0 pytest -v       # GUI bilan (agar grafik muhit bo'lsa)
HEADLESS=1 pytest -v       # headless

## GitHub Actions
- Kodingizni `main` ga push qilsangiz, workflow avtomatik ishga tushadi.
