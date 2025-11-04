# Database Setup Guide

## Step 1: Install MySQL (if not already installed)

### Option A: Using Homebrew (Recommended for macOS)

```bash
# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Set root password (if prompted or run securely)
mysql_secure_installation
```

### Option B: Using MySQL Installer

Download and install from: https://dev.mysql.com/downloads/mysql/

## Step 2: Verify MySQL is Running

```bash
# Check if MySQL is running
brew services list | grep mysql

# Or check processes
ps aux | grep mysql

# Test connection
mysql -u root -p
```

## Step 3: Create the Database

```bash
# Navigate to the assignment5 directory
cd assignments/assignment5

# Create database and tables
mysql -u root -p < schema.sql
```

You will be prompted for your MySQL root password.

## Step 4: Verify Database Creation

```bash
# Connect to MySQL
mysql -u root -p

# In MySQL prompt, run:
SHOW DATABASES;
USE rideshare_db;
SHOW TABLES;
```

You should see:
- Database: `rideshare_db`
- Tables: `USER`, `DRIVER`, `RIDER`, `RIDE`

## Step 5: (Optional) Load Sample Data

```bash
# Run the sample data script
python3 sample_data.py
```

You'll be prompted for your MySQL password.

## Step 6: Test Connection

```bash
# Run the connection test script
python3 test_db_connection.py
```

This will help diagnose any connection issues.

## Troubleshooting

### MySQL is not running

```bash
# Start MySQL service
brew services start mysql

# Or manually start
mysql.server start
```

### Can't connect - Wrong Password

1. Make sure you're using the correct MySQL root password
2. If you forgot the password, you may need to reset it

### Database doesn't exist

Make sure you ran `schema.sql` to create the database:
```bash
mysql -u root -p < schema.sql
```

### Connection refused

This usually means MySQL server is not running:
```bash
brew services start mysql
```

### Permission denied

Make sure your MySQL user has permissions:
```sql
GRANT ALL PRIVILEGES ON rideshare_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Alternative: Use SQLite (for testing only)

If you have trouble with MySQL, you can modify the code to use SQLite for local testing, but **this is not recommended** for the assignment as it requires MySQL.

## Getting Help

If you continue to have issues:
1. Run `python3 test_db_connection.py` and check the output
2. Verify MySQL is running: `brew services list`
3. Check MySQL logs if available
4. Make sure the database was created successfully

