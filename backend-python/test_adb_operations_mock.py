import unittest
from unittest.mock import patch, MagicMock
from adb_operations import ADBOperations, ADBError

class TestADBOperationsBatch(unittest.TestCase):
    def setUp(self):
        self.adb = ADBOperations()

    @patch.object(ADBOperations, '_run_command')
    def test_get_device_info_batched(self, mock_run_command):
        def mock_run(cmd, timeout=30):
            if "devices" in cmd:
                return "List of devices attached\n123456789 device"
            if "shell" in cmd and 'getprop ro.product.model' in cmd[2]:
                return "MockModel\nMockProduct\nMockManufacturer\nMockVersion"
            return ""
        mock_run_command.side_effect = mock_run

        info = self.adb.get_device_info()
        self.assertEqual(info["name"], "123456789")
        self.assertEqual(info["model"], "MockModel")
        self.assertEqual(info["product"], "MockProduct")
        self.assertEqual(info["manufacturer"], "MockManufacturer")
        self.assertEqual(info["androidVersion"], "MockVersion")

if __name__ == '__main__':
    unittest.main()
