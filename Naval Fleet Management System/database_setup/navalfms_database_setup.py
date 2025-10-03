import mysql.connector as connector
import getpass
import sys
import os

def resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


while True:
    try:
        host = input("Enter MySQL host: ")
        password = getpass.getpass("Enter MySQL root password: ")

        if host == "":
            host = "127.0.0.1"
        if password == "":
            password = "root"

        conn = connector.connect(
            host=host,
            user="root",
            password=password
        )

        cursor = conn.cursor()

        sql_file_path = resource_path("NavalFMS.sql")

        with open(sql_file_path, "r") as file:
            sql = file.read()

        commands = [cmd.strip() for cmd in sql.split(";") if cmd.strip()]

        for command in commands:
            cursor.execute(command)

        print("Database setup completed successfully.")

        cursor.close()
        conn.close()

        break

    except connector.Error as e:
        print(f"Could not connect to the server: {e}")
        if input("Try again? (y/n): ").lower() != "y":
            break

input("Press Enter to exit...")
