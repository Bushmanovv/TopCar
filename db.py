import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",        # or change to your MySQL host
        user="root",             # replace if your MySQL username is different
        password="Karim123!",             # replace with your MySQL password
        database="car_dealership"
    )
