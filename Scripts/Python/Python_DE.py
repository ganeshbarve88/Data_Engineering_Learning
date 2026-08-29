# These examples bridge the gap between "basic syntax" and "real-world data extraction."

# ### 1. Handling "Configuration" (Dictionaries)

# In your extraction script, you used a dictionary to store `DB_CONFIG`. Understanding how to access this data is essential for modularizing your code.

# ```python
def connect_db(config):
    # Accessing values from the dictionary
    print(f"Connecting to {config['dbname']} on host {config['host']}...")

if __name__ == "__main__":
    db_settings = {
        "dbname": "pagila_db",
        "user": "my_user",
        "host": "localhost"
    }
    connect_db(db_settings)

```

### 2. Iterating over a List of Tables (For Loops)

In your script, you loop through a list of tables to extract them one by one. This is exactly how you handle batch processing.

```python
def process_tables(table_list):
    for table in table_list:
        # Imagine this part calling your SQL query
        print(f"Starting extraction for table: {table.upper()}")
        print(f"Saving data to: seeds/{table}.csv")

if __name__ == "__main__":
    my_tables = ["actor", "film", "address", "customer"]
    process_tables(my_tables)

```

### 3. Using `with` Statements (Context Managers)

Your script uses `with open(...)` to handle files. This is a best practice because it automatically closes the file, even if an error occurs.

```python
def write_header(filename, headers):
    # The 'with' block ensures the file closes automatically
    with open(filename, 'w') as f:
        f.write(",".join(headers) + "\n")
        print(f"Header written to {filename}")

if __name__ == "__main__":
    write_header("seeds/actor.csv", ["actor_id", "first_name", "last_name"])

```

### 4. Error Handling (Try-Except)

Database connections are fragile. Your extraction script needs to handle cases where the server is down, so the whole program doesn't "crash" without a helpful message.

```python
def safe_extract():
    try:
        # Simulating a DB connection
        raise ConnectionError("Could not connect to PostgreSQL!")
    except ConnectionError as e:
        print(f"Oops! Data Engineering Error: {e}")
    finally:
        print("Closing any open database connections...")

if __name__ == "__main__":
    safe_extract()

```

### 5. String Formatting (F-Strings)

You use f-strings to build your SQL queries dynamically. This is the cleanest way to insert variables into your SQL code.

```python
def build_query(table_name):
    # Using f-strings to dynamically create the SQL
    query = f"SELECT * FROM {table_name} LIMIT 100;"
    return query

if __name__ == "__main__":
    table = "film"
    print(f"Generated SQL: {build_query(table)}")

```

---

### Why these are the "Data Engineer's Toolbox":

* **Dictionaries** store your credentials safely.
* **For Loops** allow you to scale your script from one table to one hundred tables without changing the code.
* **With Statements** ensure you don't corrupt your CSV files by leaving them "open" if the script crashes.
* **Try/Except** provides the observability you need when debugging why a pipeline failed at 2:00 AM.
* **F-Strings** make your SQL queries readable and maintainable.

Does seeing how these patterns directly apply to your `extract_to_csv.py` script help your student see why these concepts are so important?