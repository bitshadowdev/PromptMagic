
import unittest
from unittest.mock import patch, MagicMock
from src.plugins.openapi.openapi_plugin import OpenAPIPlugin

class TestOpenAPIPlugin(unittest.TestCase):

    @patch('requests.get')
    def test_get_openapi_spec(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"info": {"title": "Test API"}}'
        mock_get.return_value = mock_response

        plugin = OpenAPIPlugin()
        spec = plugin.get_openapi_spec("http://fakeapi.com/swagger.json")

        self.assertIsNotNone(spec)
        self.assertEqual(spec, '{"info": {"title": "Test API"}}')

    @patch('requests.get')
    def test_get_openapi_spec_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        plugin = OpenAPIPlugin()
        spec = plugin.get_openapi_spec("http://fakeapi.com/swagger.json")

        self.assertIsNone(spec)

if __name__ == '__main__':
    unittest.main()
