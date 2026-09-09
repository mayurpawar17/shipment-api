import psycopg

#Test the connection

#psycopg is a PostgreSQL driver for Python.

connection = psycopg.connect(
    "postgresql://postgres:postgres@localhost:5432/mydb"
)

print("Database connected successfully!")

connection.close()