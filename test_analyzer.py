import unittest
from analyzer import analyze


class AnalyzerTests(unittest.TestCase):
    def test_plain_domain(self):
        self.assertEqual(analyze('example.com')['score'], 0)

    def test_impersonation(self):
        self.assertGreaterEqual(analyze('http://paypal.com.verify-account.example/login')['score'], 4)

    def test_user_info(self):
        result = analyze('https://google.com@evil.example')
        self.assertEqual(result['host'], 'evil.example')
        self.assertGreaterEqual(result['score'], 4)

    def test_unicode(self):
        self.assertIn('xn--', analyze('https://аpple.com')['host'])

    def test_ipv6(self):
        self.assertGreater(analyze('https://[::1]')['score'], 0)

    def test_download(self):
        self.assertGreater(analyze('https://example.com/setup.exe')['score'], 0)

    def test_invalid(self):
        for value in ['', None, 'javascript:alert(1)', 'not a url', 'https://example.com:99999', 'https://exa%mple.com']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                analyze(value)


if __name__ == '__main__':
    unittest.main()
