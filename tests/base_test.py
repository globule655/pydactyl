import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from pydactyl.api.base import PterodactylAPI


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.api = PterodactylAPI(url='https://dummy.com', api_key='dummy_key')

    def test_init(self):
        self.assertEqual('dummy_key', self.api._api_key)
        self.assertEqual('https://dummy.com/api', self.api._url)

    def test_get_headers(self):
        expected = {
            'Authorization': 'Bearer dummy_key',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.assertDictEqual(expected, self.api._get_headers())

    def test_url_join(self):
        self.assertEqual('www.test.com/path', self.api._url_join(
            'www.test.com', 'path'))
        self.assertEqual('test.com/path/to/thing',
                         self.api._url_join('test.com', 'path', 'to', 'thing'))
        self.assertEqual('https://asdf.com/api/other/things',
                         self.api._url_join('https://asdf.com', '/api/',
                                            'other/things'))

    @mock.patch('requests.get')
    def test_valid_api_get_request(self, mock_request):
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='nomorecoffee')
        mock_request.assert_called_with('https://dummy.com/api/nomorecoffee',
                                        **expected)

    @mock.patch('requests.post')
    def test_valid_api_post_request(self, mock_request):
        data = {'test': 'data'}
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='foo', mode='POST', data=data)
        mock_request.assert_called_with('https://dummy.com/api/foo', json=data,
                                        **expected)

    @mock.patch('requests.patch')
    def test_valid_api_patch_request(self, mock_request):
        data = {'patch': 'me'}
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='bar', mode='PATCH', data=data)
        mock_request.assert_called_with('https://dummy.com/api/bar', json=data,
                                        **expected)

    @mock.patch('requests.delete')
    def test_valid_api_delete_request(self, mock_request):
        expected = {
            'params': None,
            'headers': self.api._get_headers(),
        }
        self.api._api_request(endpoint='havecoffee', mode='DELETE')
        mock_request.assert_called_with('https://dummy.com/api/havecoffee',
                                        **expected)
