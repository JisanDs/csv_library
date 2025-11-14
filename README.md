# 📚 cfu: CSV File Utilities Library

Hello, World\! My name is **Jisan**, and this is my practice project, the **cfu (CSV File Utilities) library**.

I created this library as a **Quick Recap** after finishing my Python learning journey and before starting to learn SQL. The primary goal is to **make CSV file handling easier** by using dictionary-based data formats, allowing for quick and straightforward CRUD (Create, Read, Update, Delete) operations.

> **My goal is to become a Data Scientist**, and this project represents a significant step towards that objective.

-----

## 🏗️ Project Structure

```
cfu/
├── __init__.py
├── cfu.py                    # Core library code (BasicCsv, ColMan)
Unit Tests/
├── unit_test.py              # Unit test file
Project using cfu lab/
├── products_manager.py       # A project built using the cfu library
├── products.csv
README.md                     # This file
.gitignore
config.toml                   # Configuration file (for future use)
```

-----

## 1️⃣ cfu (CSV File Utilities) Library

The `cfu` library contains two main classes that handle the necessary CSV operations:

### 🌟 Key Features

  * **Simple Data Access:** Data is accessed as dictionaries, which is idiomatic for Python.
  * **Built-in Persistence:** Automatic calling of `save_csv` ensures changes made to the in-memory data (`self.data`) are synchronized with the file.
  * **Robust Sorting:** Capability to perform numeric or string sorting based on a specified column.
  * **Column Manipulation:** A dedicated class (`ColMan`) for adding, deleting, or renaming columns.

### `BasicCsv` Class

Handles fundamental CSV file operations such as:

  * `save_csv`: Saving data to the file.
  * `_load_csv`: Loading data from the file.
  * `search_column`: Searching for a value within a column.
  * `del_data`: Deleting rows that match a specific value.

### `ColMan` (Column Manipulation) Class

Dedicated to column-specific operations:

  * `add_column`: Adding a new column at the end.
  * `add_column_position`: Inserting a column at a specific index/position.
  * `rename_column`: Changing a column's header name.

-----

## 2️⃣ Unit Tests

The `Unit Tests/unit_test.py` file contains test cases designed to ensure the library's functionality.

These tests guarantee the **Reliability** of the code by checking:

  * Successful file loading and saving.
  * Correct row counting.
  * Accurate sorting logic (for both string and numeric types).
  * Data and field consistency after column addition, deletion, or renaming.

**Unit testing is crucial for ensuring code quality and long-term maintainability.**

-----

## 3️⃣ Practical Application (Project using cfu lab)

The `Project using cfu lab/products_manager.py` file is a simple project demonstrating the use of the `cfu` library.

This project showcases **how few lines of code** were needed thanks to the `cfu` library. The benefits of using the library are clear:

  * **Reusability:** Instead of rewriting common operations (like data updating), only the library methods are called.
  * **Abstraction:** It abstracts away the complexities of file I/O, raw `csv` module handling, and basic error handling.

I believe this practical application is **even more effective than the unit tests** in proving the library's capability—it shows how easily it can be used in a real-world scenario.

-----

## 🛣️ Future Scope / Roadmap

To make this project even more robust and professional, I have the following plans:

  * **TOML Integration:** Implement loading of configuration settings (like default file names, fields) from the `config.toml` file instead of hardcoding them.
  * **Data Validation:** Add functions for validating data types when rows or columns are added.
  * **Better Error Handling:** Implement clearer exception handling beyond `FileNotFoundError` and `KeyError`.
  * **Full Documentation:** Generate comprehensive documentation using tools like Sphinx.

-----

## 🤝 Contribution

I am currently in the learning process, and **Data Science** is my ultimate goal. Any suggestions or code contributions to improve this project are welcome and appreciated.

Thank you\!