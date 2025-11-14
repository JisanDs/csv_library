import csv
import os


FILE = "default.csv"
FIELDS = ['id', 'name', 'age']


class BasicCsv:
    """
    This BasicCsv class provides fundamental utilities for handling CSV files
    using dictionary format (DictReader/DictWriter).
    
    Attributes:
        file_name (str): The name of the CSV file currently being handled.
        fields (list): A list of column headers (fieldnames).
        data (list of dict): The in-memory representation of the CSV data.
    
    Functions:
    - save_csv : Saves the in-memory data back to the CSV file.
    - add_data : Interactively adds a new row to the data and file.
    - count_row : Returns the number of rows.
    - search_column : Searches for a specific value in a column.
    - sort_by : Sorts the data based on a column key.
    - del_data : Deletes rows matching a specific value.
    - update_value : Updates a specific value across matching rows.
    """

    def __init__(self, file_name=FILE, fields=FIELDS):
        """
        Initializes the BasicCsv handler. Loads data from the specified file.
        
        Parameters:
            file_name (str, optional): The path to the CSV file. 
                                       Default is 'default.csv' (FILE constant).
            fields (list, optional): A list of expected column headers. 
                                     Default is ['id', 'name', 'age'] (FIELDS constant).
        
        Returns:
            None
        """
        self.file_name = file_name
        self.fields = fields
        self.data = self._load_csv(self.file_name)

    def _load_csv(self, file_name):
        """
        Loads data from the CSV file into memory (self.data). 
        Updates self.fields with fieldnames found in the file if it exists.
        
        Parameters:
            file_name (str): The path to the CSV file to load.
            
        Returns:
            list of dict: The data read from the CSV file. Returns an empty list
                          if the file does not exist.
        """
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
        """
        Saves the provided data (or self.data if None) to the specified CSV file.
        
        Parameters:
            data (list of dict, optional): The data to save. If None, uses self.data.
            file_name (str, optional): The file name to save to. If None, uses self.file_name.
            fields (list, optional): The list of fieldnames (headers). If None, uses self.fields.
            
        Returns:
            None
        """
        data = data if data is not None else self.data
        file_name = file_name if file_name else self.file_name
        fields = fields if fields else self.fields

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

    def add_data(self):
        """
        Adds a new row to the CSV by prompting the user for input 
        for each column defined in self.fields. Updates both self.data 
        and the CSV file (appending mode).
        
        Parameters:
            (No arguments passed directly; relies on interactive user input via input())
            
        Returns:
            None
        """
        new_data = {}
        for field in self.fields:
            value = input(f"{field.capitalize()}: ")
            new_data[field] = value

        self.data.append(new_data)

        with open(self.file_name, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow(new_data)

    def count_row(self):
        """
        Returns the number of rows currently loaded in self.data.
        
        Parameters:
            (None)
            
        Returns:
            int: The total count of data rows.
        """
        return len(self.data)

    def search_column(self, col_name, value):
        """
        Searches for the first row where the specified column matches the given value.
        
        Parameters:
            col_name (str): The name of the column to search within.
            value (str): The value to search for.
            
        Returns:
            dict or bool or None: Returns the matching row (dict) if found. 
                                  Returns False if col_name does not exist. 
                                  Returns None if the value is not found in the column.
        """
        if col_name not in self.fields:
            return False

        for row in self.data:
            if row[col_name] == value:
                return row
        return None

    def sort_by(self, file_name=None, key='name', reverse=False):
        """
        Loads data from the file, sorts it based on the given key, and returns the sorted data.
        Attempts to sort numerically first (float conversion); otherwise, sorts as a string.
        
        Parameters:
            file_name (str, optional): The file to load data from. If None, uses self.file_name.
            key (str, optional): The column name to sort by. Default is 'name'.
            reverse (bool, optional): If True, sorts in descending order. Default is False (ascending).
            
        Returns:
            list of dict: The sorted data. Returns an empty list if the file has no data.
            
        Raises:
            FileNotFoundError: If the specified file_name does not exist.
            KeyError: If the sorting key does not exist in the data's fieldnames.
        """
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
        """
        Deletes all rows where the value in the specified key column matches del_value. 
        Updates both the CSV file and self.data.
        
        Parameters:
            del_value (str or int): The value to match for deletion. Converted to string for comparison.
            key (str, optional): The column name used for matching/deletion. Default is 'name'.
            file_name (str, optional): The file to operate on. If None, uses self.file_name.
            
        Returns:
            None
            
        Raises:
            FileNotFoundError: If the specified file_name does not exist.
        """
        file_name = file_name if file_name else self.file_name

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} Not found")

        data = self._load_csv(file_name)

        filtered = [row for row in data if row[key] != str(del_value)]
        self.save_csv(filtered, file_name=file_name)
        self.data = filtered

    def update_value(self, column, old_value, new_value, file_name=None):
        """
        Updates the value in the specified 'column' from 'old_value' to 'new_value' 
        for all matching rows. Updates both the CSV file and self.data (implicitly 
        via _load_csv, although data update happens on loaded 'data' then saved).
        
        Parameters:
            column (str): The column name where the update should happen.
            old_value (str): The existing value to be replaced.
            new_value (str): The new value to insert.
            file_name (str, optional): The file to operate on. If None, uses self.file_name.
            
        Returns:
            None
            
        Raises:
            FileNotFoundError: If the specified file_name does not exist.
        """
        file_name = file_name if file_name else self.file_name

        if not os.path.exists(file_name):
            raise FileNotFoundError(f"{file_name} Not found")

        data = self._load_csv(file_name)

        for row in data:
            if row[column] == old_value:
                row[column] = new_value

        self.save_csv(data, file_name=file_name)


class ColMan(BasicCsv):
    """
    ColMan (Column Manipulation) inherits from BasicCsv and adds specific
    functionality for manipulating column headers and their associated data.
    
    Functions:
    - add_column: Adds a new column at the end of the fields list.
    - add_column_position: Adds a new column at a specified index/position.
    - value_update: Updates a specific column value based on a row identifier match.
    - rm_column: Removes a column from the data and fields list.
    - rename_column: Renames an existing column header.
    """

    def add_column(self, col_name, value=None):
        """
        Adds a new column to the end of the field list and assigns a default value 
        to that column in all rows of self.data. Updates the CSV file.
        
        Parameters:
            col_name (str): The name of the new column to add.
            value (any, optional): The default value to set for the new column in all rows. 
                                   Default is None.
            
        Returns:
            None
        """
        if col_name not in self.fields:
            self.fields.append(col_name)

        for row in self.data:
            row[col_name] = value

        self.save_csv(self.data)

    def add_column_position(self, col_name, position, value=None):
        """
        Adds a new column at a specific index/position in the fields list and 
        assigns a default value to that column in all rows of self.data. 
        If the column already exists, it is moved to the new position.
        
        Parameters:
            col_name (str): The name of the new column to add.
            position (int): The zero-based index where the column should be inserted.
            value (any, optional): The default value to set for the new column in all rows. 
                                   Default is None.
            
        Returns:
            None
        """
        if col_name not in self.fields:
            for row in self.data:
                row[col_name] = value

        if col_name in self.fields:
            self.fields.remove(col_name)

        self.fields.insert(position, col_name)
        self.save_csv(self.data)

    def value_update(self, target_name, target_column, new_value, row_identifier="name"):
        """
        Updates a column value (target_column) in rows where the value in the 
        row_identifier column matches target_name. Updates the CSV file.
        
        Parameters:
            target_name (str): The value to match in the row_identifier column 
                               (e.g., 'Robart' if row_identifier is 'name').
            target_column (str): The name of the column whose value will be changed.
            new_value (str): The new value to set.
            row_identifier (str, optional): The column name used to identify the target row(s). 
                                            Default is 'name'.
            
        Returns:
            bool: True if at least one row was updated, False otherwise (e.g., if target_column 
                  does not exist or no matching row was found).
        """
        if target_column not in self.fields:
            return False

        updated = False
        for row in self.data:
            if row[row_identifier] == target_name:
                row[target_column] = new_value
                updated = True

        if updated:
            self.save_csv(self.data)
        return updated

    def rm_column(self, col_name):
        """
        Removes the specified column from both the fields list and all rows in self.data. 
        Updates the CSV file.
        
        Parameters:
            col_name (str): The name of the column to remove.
            
        Returns:
            bool: True if the column was successfully removed, False if col_name was not found.
        """
        if col_name not in self.fields:
            return False

        for row in self.data:
            row.pop(col_name, None)

        self.fields.remove(col_name)
        self.save_csv(self.data)
        return True

    def rename_column(self, old_name, new_name):
        """
        Renames a column header (old_name) to new_name in both the fields list and all rows in self.data.
        Updates the CSV file.
        
        Parameters:
            old_name (str): The current name of the column.
            new_name (str): The desired new name for the column.
            
        Returns:
            bool: True if the column was successfully renamed, False if old_name was not found.
        """
        if old_name not in self.fields:
            return False

        for row in self.data:
            row[new_name] = row.pop(old_name)

        idx = self.fields.index(old_name)
        self.fields[idx] = new_name
        self.save_csv(self.data)
        return True