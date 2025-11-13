"""
CSV File Utilities Library


This is a simple object oriented base csv file utilities library. There are two classes here where one is BasicCsv file handling, and the second is ColMan which means column manipulation. ColMan is very simple but has some useful functions.

For example, BasicCsv class includes data adding, saving (saving existing data), searching data, filtering through sort_by function etc.

In addition, ColMan has some functions for column manipulation. For example, there are some other functions like adding, removing columns etc.
"""


import csv
import os


FILE = "default.csv"
FIELDS = ['id', 'name', 'age']


class BasicCsv:
    """
    This BasicCsv class have Basic CSV file handling utilities.
    -> functions:
    - save_csv : save 
    - add_data
    - count_row
    - search_column
    - sort_by
    - del_data
    - update_value
    """

    def __init__(self, file_name=FILE, fields=FIELDS):
        self.file_name = file_name
        self.fields = fields
        self.data = self._load_csv(self.file_name)

    def _load_csv(self, file_name):
        """Load data from CSV file"""
        data = []
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames:
                    self.fields = reader.fieldnames
                for row in reader:
                    data.append(row)
        return data

    def save_csv(self, data=None, file_name=None, fields=None):
        """Save CSV file"""
        data = data if data is not None else self.data
        file_name = file_name if file_name else self.file_name
        fields = fields if fields else self.fields

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

    def add_data(self):
        """Add new row to CSV"""
        new_data = {}
        for field in self.fields:
            value = input(f"{field.capitalize()}: ")
            new_data[field] = value

        self.data.append(new_data)

        with open(self.file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(new_data)

    def count_row(self):
        """Return number of rows"""
        return len(self.data)

    def search_column(self, col_name, value):
        """Search a value inside a column"""
        if col_name not in self.fields:
            return False

        for row in self.data:
            if row[col_name] == value:
                return row
        return None

    def sort_by(self, file_name=None, key='name', reverse=False):
        """Sort data by column key"""
        file_name = file_name if file_name else self.file_name

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} Not found")

        data = self._load_csv(file_name)

        if not data:
            return []

        if key not in data[0]:
            raise KeyError(f"{key} Not exists in {file_name}")

        try:
            return sorted(data, key=lambda x: float(x[key]), reverse=reverse)
        except ValueError:
            return sorted(data, key=lambda x: x[key], reverse=reverse)

    def del_data(self, del_value, key="name", file_name=None):
        """Delete row using value match"""
        file_name = file_name if file_name else self.file_name

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} Not found")

        data = self._load_csv(file_name)

        filtered = [row for row in data if row[key] != str(del_value)]
        self.save_csv(filtered, file_name=file_name)

    def update_value(self, column, old_value, new_value, file_name=None):
        """Update a value in a given column"""
        file_name = file_name if file_name else self.file_name

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} Not found")

        data = self._load_csv(file_name)

        for row in data:
            if row[column] == old_value:
                row[column] = new_value

        self.save_csv(data, file_name=file_name)


class ColMan(BasicCsv):
    """ColMan = Column manipulation utilities
    This ColMan class creat mainle creat for manipulat the column.
    
    Class functions:
    - add_column : this add new column at the end
    - add_column_position : add column in your giving position
    - value_update : update your giving existing value
    - rm_column : remove your giving column
    - rename_column : rename your givin column
    """

    def add_column(self, col_name, value=None):
        if col_name not in self.fields:
            self.fields.append(col_name)

        for row in self.data:
            row[col_name] = value

        self.save_csv(self.data)

    def add_column_position(self, col_name, position, value=None):
        if col_name not in self.fields:
            for row in self.data:
                row[col_name] = value

        if col_name in self.fields:
            self.fields.remove(col_name)

        self.fields.insert(position, col_name)
        self.save_csv(self.data)

    def value_update(self, target_name, target_column, new_value, row="name"):
        """Update a column value using name match"""
        if target_column not in self.fields:
            return False

        updated = False
        for row in self.data:
            if row[row] == target_name:
                row[target_column] = new_value
                updated = True

        if updated:
            self.save_csv(self.data)
        return updated

    def rm_column(self, col_name):
        """Remove a column"""
        if col_name not in self.fields:
            return False

        for row in self.data:
            row.pop(col_name, None)

        self.fields.remove(col_name)
        self.save_csv(self.data)
        return True

    def rename_column(self, old_name, new_name):
        """Rename a column"""
        if old_name not in self.fields:
            return False

        for row in self.data:
            row[new_name] = row.pop(old_name)

        idx = self.fields.index(old_name)
        self.fields[idx] = new_name
        self.save_csv(self.data)
        return True
