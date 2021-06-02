import unittest
from config import Config
from pprint import pprint


class TestConfig(unittest.TestCase):
    def has_uri(self):
        config = Config()
        has_keys = True
        for key in ["db_uri"]:
            if key not in config.keys():
                has_keys = False
        self.assertTrue(has_keys)
        pprint(config)

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == "__main__":
    unittest.main()
