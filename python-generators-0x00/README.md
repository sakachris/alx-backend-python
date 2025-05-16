# Python Generators — MySQL Seeder

This project sets up and seeds a MySQL database with sample user data using Python. It's part of an exploration into Python generators and database integration.

## 📁 Project Structure

- `seed.py`: Contains all logic for:
  - Connecting to MySQL
  - Creating the database `ALX_prodev`
  - Creating the `user_data` table (if it doesn't exist)
  - Reading a CSV file and inserting users into the table with generated UUIDs
- `0-main.py`: Entry script that runs the setup and displays a sample of inserted data
- `user_data.csv`: Sample data used to populate the `user_data` table
- `README.md`: Project documentation

## 🛠️ Requirements

- Python 3.8+
- `mysql-connector-python` (install via `pip install mysql-connector-python`)
- MySQL server running and accessible
