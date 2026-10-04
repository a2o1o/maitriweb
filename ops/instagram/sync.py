"""Fetch the public feed without placing Instagram credentials in the web root."""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

ACCOUNT = 'maitri_aspiring_together'
GRAPH = 'https://graph.instagram.com'


def atomic_write(path, payload, mode=0o644):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(payload)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def api(path, token, **params):
    request = Request(GRAPH + path + '?' + urlencode(params),
                      headers={'Authorization': 'Bearer ' + token})
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if 'error' in result:
        raise ValueError('Instagram API rejected the request')
    return result


def download(url):
    host = urlsplit(url)
    if host.scheme != 'https' or not any(
            (host.hostname or '').endswith('.' + domain)
            for domain in ('cdninstagram.com', 'fbcdn.net')):
        raise ValueError('Unexpected image host')
    with urlopen(Request(url), timeout=30) as response:
        content_type = response.headers.get_content_type()
        extension = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}.get(content_type)
        if not extension:
            raise ValueError('Unsupported image type')
        data = response.read(15 * 1024 * 1024 + 1)
    if not data or len(data) > 15 * 1024 * 1024:
        raise ValueError('Invalid image size')
    return data, extension


def sync(config_path, output):
    config = json.loads(config_path.read_text(encoding='utf-8'))
    token = config['access_token']
    version = config['api_version']
    if not re.fullmatch(r'v\d+\.\d+', version):
        raise ValueError('Invalid API version')
    # Long-lived tokens must be at least 24 hours old before refresh.
    if time.time() - config['token_saved_at'] >= 7 * 86400:
        refreshed = api('/refresh_access_token', token,
                        grant_type='ig_refresh_token', access_token=token)
        token = refreshed['access_token']
        config.update(access_token=token, token_saved_at=time.time())
        atomic_write(config_path, json.dumps(config).encode(), 0o600)
    account = api('/' + version + '/me', token, fields='user_id,username')
    if account.get('username') != ACCOUNT:
        raise ValueError('Connected account is not Maitri')
    result = api('/' + version + '/' + str(account['user_id']) + '/media', token,
                 fields='id,caption,media_type,media_url,thumbnail_url,permalink,timestamp', limit=25)
    posts = []
    items = sorted(result['data'], key=lambda item: item['timestamp'], reverse=True)
    for item in items:
        if len(posts) == 6:
            break
        image = item.get('thumbnail_url') if item['media_type'] == 'VIDEO' else item.get('media_url')
        if not image:
            continue
        link = urlsplit(item['permalink'])
        if link.scheme != 'https' or link.hostname != 'www.instagram.com':
            raise ValueError('Unexpected post link')
        data, ext = download(image)
        filename = hashlib.sha256(data).hexdigest() + '.' + ext
        atomic_write(output / filename, data)
        posts.append({'caption': item.get('caption', ''), 'permalink': item['permalink'],
                      'timestamp': item['timestamp'], 'image': 'assets/data/instagram/' + filename})
    if items and not posts:
        raise ValueError('No usable post images returned')
    # Publish only after the entire new feed is ready; failures preserve the last feed.
    feed = {'updated_at': datetime.now(timezone.utc).isoformat(), 'posts': posts}
    atomic_write(output / 'feed.json', json.dumps(feed, ensure_ascii=True).encode())
    print('Published %d Instagram posts.' % len(posts))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=Path('/var/lib/maitri-instagram/credentials.json'))
    parser.add_argument('--output', type=Path, default=Path('/var/www/maitriweb/assets/data/instagram'))
    args = parser.parse_args()
    try:
        sync(args.config, args.output)
    except Exception as error:
        # HTTP exceptions can include token-bearing URLs. Never log exception text.
        print('Instagram sync failed (%s). Existing feed retained; check authorization and network.' % type(error).__name__, file=sys.stderr)
        sys.exit(1)
