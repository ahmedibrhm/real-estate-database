# Real Estate Management System

This is a Python project that uses SQLAlchemy and SQLite to manage a real estate database. It provides functionality for creating, inserting, and querying data related to offices, agents, sellers, buyers, listings, sales, and commissions.

## Running the code

### Create and activate a virtual environment

#### macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python3 -m venv venv
venv\Scripts\activate
```

### Install the required packages

```bash
pip3 install -r requirements.txt
```

## Usage

The following commands will create the database, insert data, and query the data:

```bash
python3 create.py
python3 insert_data.py
python3 query_data.py
```

## Running Unittests

To run all unittests in the project directory, follow these steps:

1. Open a terminal/command prompt.
2. Navigate to the project directory containing the tests folder.
3. Run the following command:

```bash
python3 -m unittest discover -s tests
```

This command will discover and run all unittests within the tests directory. The -s flag specifies the directory where unittests are located.

## Directory Structure

```bash
├── create.py
├── insert_data.py
├── query_data.py
├── utils.py
└── tests/
    ├── test_db_structure.py
    └── test_query_data.py
```
