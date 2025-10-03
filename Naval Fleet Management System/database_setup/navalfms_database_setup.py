import mysql.connector as connector
import getpass

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

        with open("Naval Fleet Management System/database_setup/NavalFMS.sql", "r") as file:
            sql = file.read()

        commands = [cmd.strip() for cmd in sql.split(";") if cmd.strip()]

        for command in commands:
            cursor.execute(command)

        conn.commit()
        print("Database setup completed successfully.")

        cursor.close()
        conn.close()
        break

    except connector.Error as e:
        print(f"Could not connect to the server: {e}")
        if input("Try again? (y/n): ").lower() != 'y':
            break

input("Press Enter to exit...")
