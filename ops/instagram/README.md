# Maitri Instagram feed

The homepage reads a public JSON cache. Credentials stay outside nginx's web root.
The timer runs Monday and Thursday at 09:00 Asia/Kolkata, with one catch-up run
after downtime. Token refresh happens within the same job, no hourly polling.

## Connect the owner account

1. In Meta for Developers, create/configure an app with Instagram API with
   Instagram Login. Connect the Creator account `maitri_aspiring_together`.
2. Authorize profile and media read access (`instagram_business_basic`). Follow
   the dashboard's account-role/tester steps for your own account. Review/access
   requirements depend on the app's configuration.
3. Obtain a long-lived token using Meta's dashboard or documented token exchange.
   Do not put the token in Git, browser JavaScript, chat or command arguments.
4. Run `sudo -u maitri-instagram python3 /opt/maitri-instagram/connect.py` in a
   private interactive server terminal. The token prompt hides input.
5. Run `sudo systemctl start maitri-instagram.service`, check the status and the
   public feed, then enable the timer with
   `sudo systemctl enable --now maitri-instagram.timer`.

## Server installation (Debian)

Run from the deployed repository as an administrator:

```sh
sudo useradd --system --no-create-home --shell /usr/sbin/nologin maitri-instagram
sudo install -d -m 755 /opt/maitri-instagram
sudo install -m 644 ops/instagram/sync.py ops/instagram/connect.py /opt/maitri-instagram/
sudo install -d -o maitri-instagram -g maitri-instagram -m 700 /var/lib/maitri-instagram
sudo install -d -o maitri-instagram -g maitri-instagram -m 755 /var/www/maitriweb/assets/data/instagram
sudo install -m 644 ops/instagram/maitri-instagram.service ops/instagram/maitri-instagram.timer /etc/systemd/system/
sudo systemctl daemon-reload
```

Skip user creation if the service user already exists. Do not enable the timer
until the first authenticated sync succeeds. The initial homepage has a profile
link, not fabricated posts. Images and JSON are runtime files ignored by Git.
On failure, the existing feed remains. Reconnect if authorization is revoked.
Check failures with `systemctl status maitri-instagram.service` and
`journalctl -u maitri-instagram.service`; no access token is logged.

Run tests with `python -m unittest discover -s ops/instagram -p "test_*.py"`.

Meta references:
- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/
- https://developers.facebook.com/docs/instagram-platform/reference/refresh_access_token/
