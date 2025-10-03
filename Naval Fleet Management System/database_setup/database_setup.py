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
            host = host,
            user = "root",
            password = password
        )

        cursor = conn.cursor()

        with open("NavalFMS.sql", "r") as f:
            sql = f.read()
            commands = sql.split(";")

        for command in commands:
            cursor.execute(command)

        print("Database setup completed successfully.")

        cursor.close()
        conn.close()
        
        break
    except connector.Error as e:
        print(f"Could not connect to the server: {e}")
        if input("Try again? (y/n): ").lower() != 'y':
            break

input("Press Enter to exit...")