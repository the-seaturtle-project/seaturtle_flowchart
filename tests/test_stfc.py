import unittest
from seaturtle_flowchart.reader.stfc import STFCReader

VALID_PATH = 'tests/input.stfc'
INVALID_PATH = 'thispath/doesnt-exist.txt'

class TestSTFCReader(unittest.TestCase):
    def test_requires_file_inline(self):
        # Test 1: File exists
        reader = STFCReader(VALID_PATH)

        self.assertIsNone(reader.requires_file_inline())

        # Test 2: File does not exist
        reader = STFCReader(INVALID_PATH)

        with self.assertRaises(FileNotFoundError):
            reader.requires_file_inline()

    def test_metadata(self):
        # Test 1: Successfully read metadata
        reader = STFCReader(VALID_PATH)
        metadata = reader.metadata

        self.assertEqual(metadata, {
            'name': 'School',
            'description': "Flowchart to show show process of getting to school"
        })

        # Test 2: File not found
        reader = STFCReader(INVALID_PATH)

        with self.assertRaises(FileNotFoundError):
            metadata = reader.metadata
