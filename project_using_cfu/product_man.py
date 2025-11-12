from cfu import BasicCsv, ColMan


TEST_FILE = "test.csv"
TEST_FIELDS = ['id', 'name', 'age']
TEST_DATA = [
    {"id": "1", "name": "Alice", "age": "20"},
    {"id": "2", "name": "Bob", "age": "22"},
]


colman = ColMan()
colman.save_csv(TEST_DATA, TEST_FILE, TEST_FIELDS)