# Library Management System

## Description
The **Library Management System** is a Python-based application designed to manage library resources efficiently. It allows administrators to manage books, users, and transactions, providing an easy-to-use interface for handling library operations.

## Features
- **User Management**: Add, edit, and remove users from the system.
- **Book Management**: Add, edit, and remove books. Track availability and borrowing status.
- **Transaction Management**: Issue and return books, and track transaction history.
- **Authentication**: Secure login system for both users and administrators.
- **Database Integration**: All data is stored and managed in a structured SQL database.

## Installation

### Prerequisites
- Python 3.x
- MySQL or SQLite

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Library-Management-System.git
   cd Library-Management-System
   ```

2. **Install dependencies**:
   If your project uses any Python packages, install them using:
   ```bash
   pip install -r requirements.txt
   ```

3. **Database setup**:
   - Create a database using MySQL or SQLite.
   - Execute the SQL commands in `library.sql` to set up the necessary tables.
   - Update the database connection details in `conn.py`.

4. **Run the application**:
   Start the main application by running:
   ```bash
   python main.py
   ```

## Usage
- **Admin**: Use the admin credentials to log in and manage users, books, and transactions.
- **User**: Users can log in to view their borrowed books, due dates, and manage their profiles.

## File Structure
\`\`\`
Library-Management-System/
│
├── Library-Management-System/
│   ├── admin.py          # Admin functionalities
│   ├── conn.py           # Database connection settings
│   ├── login.py          # Login functionalities
│   ├── main.py           # Entry point of the application
│   ├── user.py           # User functionalities
│   ├── library.sql       # SQL file to set up the database
│   └── README.md         # Project documentation
│
├── .git/                 # Version control folder
└── __pycache__/          # Compiled Python files
\`\`\`

## Database Schema
The database consists of the following tables:
- **Users**: Stores user details (ID, Name, Email, Password, etc.)
- **Books**: Stores book details (ID, Title, Author, ISBN, Availability, etc.)
- **Transactions**: Tracks book issues and returns (Transaction ID, User ID, Book ID, Issue Date, Return Date)

For detailed schema, refer to the `library.sql` file.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
