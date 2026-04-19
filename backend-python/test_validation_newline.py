import unittest
from adb_operations import ADBOperations

class TestPackageNameNewline(unittest.TestCase):
    def test_newline_injection(self):
        # A payload with a newline at the end
        payload = "com.example.app\n"
        self.assertFalse(ADBOperations.is_valid_package_name(payload),
                         "Payload with newline should be invalid!")

if __name__ == '__main__':
    unittest.main()
