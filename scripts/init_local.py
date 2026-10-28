"""Create local configuration once, without printing or replacing secrets."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
target = root / '.env'
if not target.exists():
    template = (root / '.env.example').read_text()
    target.write_text(template.replace('change-me-generate-a-local-random-secret-before-starting', secrets.token_urlsafe(64)))
    print('Created .env with a random local secret.')
else:
    print('Existing .env preserved.')
