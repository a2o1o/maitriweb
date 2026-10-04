import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import sync


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = self.root / 'private.json'
        self.config.write_text(json.dumps({'access_token': 'secret-test-token',
            'api_version': 'v25.0', 'token_saved_at': time.time()}))
        self.output = self.root / 'public'
        self.output.mkdir()
        self.feed = self.output / 'feed.json'
        self.feed.write_text('{"posts": []}')

    def items(self):
        return [{'id': str(i), 'media_type': 'VIDEO' if i == 8 else 'IMAGE',
                 'media_url': 'https://example.cdninstagram.com/image',
                 'thumbnail_url': 'https://example.cdninstagram.com/thumb',
                 'permalink': 'https://www.instagram.com/p/test%d/' % i,
                 'timestamp': '2026-10-%02dT09:00:00+0000' % i,
                 'caption': 'Post %d' % i} for i in range(1, 9)]

    @patch('sync.download', return_value=(b'test-image', 'jpg'))
    @patch('sync.api')
    def test_latest_six_video_thumbnail_and_no_secrets(self, api, download):
        api.side_effect = [{'user_id': '123', 'username': sync.ACCOUNT}, {'data': self.items()}]
        sync.sync(self.config, self.output)
        feed = json.loads(self.feed.read_text())
        self.assertEqual([p['caption'] for p in feed['posts']], ['Post %d' % i for i in range(8, 2, -1)])
        self.assertEqual(download.call_args_list[0].args[0], 'https://example.cdninstagram.com/thumb')
        self.assertNotIn('secret-test-token', self.feed.read_text())
        self.assertTrue((self.output / Path(feed['posts'][0]['image']).name).exists())

    @patch('sync.download', side_effect=OSError('failed'))
    @patch('sync.api')
    def test_failure_preserves_existing_feed(self, api, download):
        old = self.feed.read_bytes()
        api.side_effect = [{'user_id': '123', 'username': sync.ACCOUNT}, {'data': self.items()}]
        with self.assertRaises(OSError):
            sync.sync(self.config, self.output)
        self.assertEqual(self.feed.read_bytes(), old)

    @patch('sync.api', return_value={'user_id': '123', 'username': 'wrong_account'})
    def test_wrong_account_rejected(self, api):
        with self.assertRaises(ValueError):
            sync.sync(self.config, self.output)

    @patch('sync.api')
    def test_refresh_persisted_privately(self, api):
        config = json.loads(self.config.read_text())
        config['token_saved_at'] = time.time() - 8 * 86400
        self.config.write_text(json.dumps(config))
        api.side_effect = [{'access_token': 'refreshed-secret'},
                           {'user_id': '123', 'username': sync.ACCOUNT}, {'data': []}]
        sync.sync(self.config, self.output)
        self.assertEqual(json.loads(self.config.read_text())['access_token'], 'refreshed-secret')
        self.assertNotIn('refreshed-secret', self.feed.read_text())

    def test_untrusted_image_host(self):
        for url in ['http://example.cdninstagram.com/a', 'https://localhost/a',
                    'https://cdninstagram.com.evil.test/a']:
            with self.assertRaises(ValueError):
                sync.download(url)


if __name__ == '__main__':
    unittest.main()
