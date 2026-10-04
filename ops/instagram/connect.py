"""Run interactively on the server; never paste credentials into chat or shell history."""
import getpass
import json
import time
from pathlib import Path
from sync import ACCOUNT, api, atomic_write

token = getpass.getpass('Long-lived Instagram access token (hidden): ').strip()
version = input('API version shown in your Meta app (for example v25.0): ').strip()
try:
    account = api('/' + version + '/me', token, fields='user_id,username')
    if account.get('username') != ACCOUNT:
        raise ValueError('Wrong account')
    atomic_write(Path('/var/lib/maitri-instagram/credentials.json'), json.dumps({
        'access_token': token, 'api_version': version, 'token_saved_at': time.time()
    }).encode(), 0o600)
    print('Maitri connected. Run the first sync to verify media access.')
except Exception:
    raise SystemExit('Connection failed. Check the account, token, API version and permissions.')
