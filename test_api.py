import unittest
from app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_check(self):
        response = self.client.post('/api/check', json={'url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['host'], 'example.com')
        self.assertEqual(response.headers['Cache-Control'], 'no-store')

    def test_invalid_payload(self):
        for value in [{}, [], {'url': 123}, {'url': 'javascript:alert(1)'}]:
            self.assertEqual(self.client.post('/api/check', json=value).status_code, 400)

    def test_content_type(self):
        self.assertEqual(self.client.post('/api/check', data='test').status_code, 415)

    def test_size_limit(self):
        self.assertEqual(self.client.post('/api/check', json={'url': 'a' * 20000}).status_code, 413)


if __name__ == '__main__':
    unittest.main()
