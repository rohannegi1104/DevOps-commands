import mysql.connector

# Connect to the MySQL database
mydb = mysql.connector.connect(
    host='localhost',  # Your MySQL server host
    user='root',       # Your MySQL username
    password='',       # Your MySQL password (provide if non-empty)
    database='python_database'  # Your database name (without spaces)
)

# Cursor to execute SQL queries
mycursor = mydb.cursor()

# Ensure the 'Student' table exists or create it
mycursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Roll_no INT,
    age INT
)
""")

# Insert multiple values into the database
ins = "INSERT INTO Student (Name, Roll_no, age) VALUES (%s, %s, %s)"
values = [
    ('sachin', 12, 24),
    ('raghav', 13, 25),
    ('rajiv', 14, 26)
]

# Execute the SQL query to insert multiple rows
mycursor.executemany(ins, values)

# Save changes to the database
mydb.commit()
print("Data inserted successfully")

# SQL query to retrieve all rows
sql = 'SELECT * FROM Student'

# Execute the SQL query
mycursor.execute(sql)

# Fetch all data
rows = mycursor.fetchall()
print("Data from database:")
for row in rows:
    print(row)

print("This is the student table")

# Close the cursor and the database connection
mycursor.close()
mydb.close()
