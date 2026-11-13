import os
import unittest
from unittest.mock import patch

from nexus_client import NexusClient, NexusConfig, NexusConfigurationError, NexusHTTPError


class NexusClientTests(unittest.TestCase):
    def test_missing_url_is_rejected(self):
        with patch.dict(os.environ, {"NEXUS_URL": "", "NEXUS_API_KEY": "secret"}, clear=False):
            with self.assertRaises(NexusConfigurationError):
                NexusConfig.from_env()

    def test_missing_key_is_rejected(self):
        with patch.dict(os.environ, {"NEXUS_URL": "https://nexus.example", "NEXUS_API_KEY": ""}, clear=False):
            with self.assertRaises(NexusConfigurationError):
                NexusConfig.from_env()

    def test_url_trailing_slash_is_normalized(self):
        config = NexusConfig("https://nexus.example/", "secret")
        self.assertEqual(config.base_url.rstrip("/"), "https://nexus.example")

    def test_http_error_is_structured(self):
        err = NexusHTTPError(401, "authentication or permission failed")
        self.assertEqual(err.status, 401)
        self.assertIn("401", str(err))


if __name__ == "__main__":
    unittest.main()
