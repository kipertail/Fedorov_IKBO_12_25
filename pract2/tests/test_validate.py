import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from main import (validate_depth, validate_output, validate_package,
                  validate_repo, validate_version)

TEST_REPO = os.path.join(os.path.dirname(__file__), "graph1.txt")


class TestValidatePackage(unittest.TestCase):

    def test_valid_name(self):
        self.assertIsNone(validate_package("libc6", False))
        self.assertIsNone(validate_package("g++-12", False))

    def test_invalid_name(self):
        self.assertIsNotNone(validate_package("Curl", False))
        self.assertIsNotNone(validate_package("-abc", False))

    def test_test_mode_name(self):
        self.assertIsNone(validate_package("A", True))
        self.assertIsNotNone(validate_package("a", True))


class TestValidateRepo(unittest.TestCase):

    def test_url(self):
        self.assertIsNone(validate_repo("https://example.com", False))
        self.assertIsNotNone(validate_repo("example.com", False))

    def test_test_file(self):
        self.assertIsNone(validate_repo(TEST_REPO, True))
        self.assertIsNotNone(validate_repo("missing.txt", True))


class TestValidateOther(unittest.TestCase):

    def test_version(self):
        self.assertIsNone(validate_version("1:2.3-4ubuntu1", False))
        self.assertIsNotNone(validate_version("", False))
        self.assertIsNotNone(validate_version("1 0", False))
        self.assertIsNone(validate_version("", True))

    def test_output(self):
        self.assertIsNone(validate_output("graph.svg"))
        self.assertIsNotNone(validate_output("graph.png"))
        self.assertIsNotNone(validate_output("nodir/graph.svg"))

    def test_depth(self):
        self.assertIsNone(validate_depth(1))
        self.assertIsNotNone(validate_depth(0))
        self.assertIsNotNone(validate_depth(-5))


if __name__ == "__main__":
    unittest.main()
