import sys
import os
import unittest
import csv
import shutil


sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from cfu import BasicCsv, ColMan

# --- Testing Constants ---
TEST_DIR = "test_temp_dir"
TEST_FILE_BASIC = os.path.join(TEST_DIR, "basic_test.csv")
TEST_FIELDS = ['id', 'name', 'score']

# --- UPDATED DATA SET ---
TEST_DATA = [
    {'id': '1', 'name': 'Robart', 'score': '90'},
    {'id': '2', 'name': 'Elon', 'score': '85'},
    {'id': '3', 'name': 'Jisan', 'score': '92'},
    {'id': '4', 'name': 'Tom', 'score': '90'}
]
# --------------------------

class TestBasicCsv(unittest.TestCase):
    """Test cases for the BasicCsv class."""
    
    @classmethod
    def setUpClass(cls):
        """Creates a temporary directory before running test cases."""
        os.makedirs(TEST_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Removes the temporary directory after all tests are done."""
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def setUp(self):
        """Creates a temporary CSV file and initializes the BasicCsv handler before each test."""
        self._write_test_csv(TEST_FILE_BASIC, TEST_FIELDS, TEST_DATA)
        self.csv_handler = BasicCsv(file_name=TEST_FILE_BASIC, fields=TEST_FIELDS)

    def tearDown(self):
        """Removes the temporary CSV file after each test (if it exists)."""
        if os.path.exists(TEST_FILE_BASIC):
            os.remove(TEST_FILE_BASIC)

    def _write_test_csv(self, file_name, fields, data):
        """Utility function to create a CSV file for testing."""
        with open(file_name, "w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
            
    # --- 1. Load and Count Tests ---

    def test_initial_load(self):
        """Verifies that __init__ and _load_csv correctly load data and fields."""
        # Check if data is loaded
        self.assertEqual(len(self.csv_handler.data), 4) 
        # Check if fields are loaded correctly
        self.assertEqual(self.csv_handler.fields, TEST_FIELDS) 
        # Check data integrity (First row is now Robart)
        self.assertEqual(self.csv_handler.data[0]['name'], 'Robart')

    def test_count_row(self):
        """Verifies that count_row returns the correct number of rows."""
        self.assertEqual(self.csv_handler.count_row(), 4)

    # --- 2. Search Tests ---

    def test_search_found(self):
        """Verifies that a record is successfully found."""
        found_row = self.csv_handler.search_column('name', 'Jisan')
        self.assertIsNotNone(found_row)
        self.assertEqual(found_row['score'], '92')

    def test_search_not_found(self):
        """Verifies that None is returned when no record is found."""
        found_row = self.csv_handler.search_column('name', 'Unknown')
        self.assertIsNone(found_row)
        
    def test_search_invalid_column(self):
        """Verifies that False is returned for an invalid column name."""
        result = self.csv_handler.search_column('age', '92') 
        self.assertFalse(result)
        
    # --- 3. Sort Tests ---

    def test_sort_by_string_key(self):
        """Verifies correct ascending sort by a string key ('name')."""
        sorted_data = self.csv_handler.sort_by(key='name', reverse=False)
        # Alphabetical order: Elon (E) -> Jisan (J) -> Robart (R) -> Tom (T)
        self.assertEqual(sorted_data[0]['name'], 'Elon') 
        
    def test_sort_by_numeric_key(self):
        """Verifies correct descending sort by a numeric key ('score')."""
        sorted_data = self.csv_handler.sort_by(key='score', reverse=True)
        # Expected order (descending score): 92 (Jisan) -> 90 (Robart/Tom) -> 85 (Elon)
        self.assertEqual(sorted_data[0]['name'], 'Jisan') 
        self.assertEqual(sorted_data[-1]['name'], 'Elon')
        
    def test_sort_invalid_key(self):
        """Verifies that KeyError is raised for an invalid sort key."""
        with self.assertRaises(KeyError): 
            self.csv_handler.sort_by(key='city') 

    # --- 4. Delete Test ---

    def test_del_data_exists(self):
        """Verifies that an existing row is successfully deleted."""
        # Note: You must ensure self.data is updated in your del_data method for this test to pass.
        self.csv_handler.del_data(del_value='Robart', key='name')
        
        # Check the in-memory data
        self.assertEqual(len(self.csv_handler.data), 3) 
        
        # Verify the deletion by searching the in-memory data
        self.assertIsNone(self.csv_handler.search_column('name', 'Robart'))

    # --- 5. Update Test ---
    
    def test_update_value(self):
        """Verifies that a value is successfully updated in the specified column."""
        self.csv_handler.update_value(column='score', old_value='90', new_value='95')
        
        # Reload data from the file to confirm persistence
        data_after_update = self.csv_handler._load_csv(TEST_FILE_BASIC)
        
        # Two records (Robart and Tom) had a score of '90' and should now be '95'
        updated_count = 0
        for row in data_after_update:
            if row['score'] == '95':
                updated_count += 1
                
        self.assertEqual(updated_count, 2)
        self.assertEqual(len(data_after_update), 4) # No rows should be deleted

# --- ColMan Class Tests ---
class TestColMan(unittest.TestCase):
    """Test cases for the ColMan (Column Manipulation) class."""
    
    @classmethod
    def setUpClass(cls):
        """Creates a temporary directory before running test cases."""
        os.makedirs(TEST_DIR, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Removes the temporary directory after all tests are done."""
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)

    def setUp(self):
        """Creates a temporary CSV file and initializes the ColMan handler before each test."""
        self._write_test_csv(TEST_FILE_BASIC, TEST_FIELDS, TEST_DATA)
        self.csv_handler = ColMan(file_name=TEST_FILE_BASIC, fields=TEST_FIELDS) 

    def tearDown(self):
        if os.path.exists(TEST_FILE_BASIC):
            os.remove(TEST_FILE_BASIC)

    def _write_test_csv(self, file_name, fields, data):
        """Utility function to create a CSV file for testing."""
        with open(file_name, "w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

    # --- 1. Add Column Tests ---

    def test_add_column_end(self):
        """Verifies that a column is successfully added to the end."""
        self.csv_handler.add_column('city', value='Dhaka')
        
        # Check in-memory data
        self.assertIn('city', self.csv_handler.fields)
        self.assertEqual(self.csv_handler.fields[-1], 'city')
        self.assertEqual(self.csv_handler.data[0]['city'], 'Dhaka')
        
    def test_add_column_position(self):
        """Verifies that a column is successfully added at the specified position."""
        self.csv_handler.add_column_position('email', 1, value='test@example.com')
        
        # Check field position (0: id, 1: email, 2: name, 3: score)
        self.assertEqual(self.csv_handler.fields[1], 'email')
        self.assertEqual(self.csv_handler.data[0]['email'], 'test@example.com')
        
    # --- 2. Remove Column Test ---

    def test_rm_column(self):
        """Verifies that a column is successfully removed."""
        result = self.csv_handler.rm_column('score')
        
        self.assertTrue(result)
        self.assertNotIn('score', self.csv_handler.fields)
        self.assertNotIn('score', self.csv_handler.data[0])
        
    # --- 3. Rename Column Test ---

    def test_rename_column(self):
        """Verifies that a column is successfully renamed."""
        result = self.csv_handler.rename_column('name', 'full_name')
        
        self.assertTrue(result)
        self.assertIn('full_name', self.csv_handler.fields)
        self.assertNotIn('name', self.csv_handler.fields)
        self.assertEqual(self.csv_handler.data[0]['full_name'], 'Robart')
        
    # --- 4. Value Update Test (ColMan) ---

    def test_value_update_found(self):
        """Verifies that a value is updated using the row_identifier (e.g., 'name')."""
        # Change Elon's score from 85 to 100
        result = self.csv_handler.value_update('Elon', 'score', '100', row_identifier='name')
        
        self.assertTrue(result)
        
        # Check in-memory data
        updated_row = self.csv_handler.search_column('name', 'Elon')
        self.assertEqual(updated_row['score'], '100')

    def test_value_update_not_found(self):
        """Verifies that no update happens and False is returned if row_identifier is not found."""
        result = self.csv_handler.value_update('Unknown', 'score', '100', row_identifier='name')
        
        self.assertFalse(result)
        
        # Check if data remains unchanged
        initial_row = self.csv_handler.search_column('name', 'Robart')
        self.assertEqual(initial_row['score'], '90')


if __name__ == '__main__':
    unittest.main()