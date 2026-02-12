import os

import mysql.connector


class DbConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv("MYSQL_HOST", "localhost"),
            'port': int(os.getenv("MYSQL_PORT", "3306")),
            'user': os.getenv("MYSQL_USER", "root"),
            'password': os.getenv("MYSQL_PASSWORD", "")
        }
        self.database = os.getenv("MYSQL_DB", "weapon_db")
        self.connection = None

    def get_connection(self):
        self.connection = mysql.connector.connect(**self.config)

        if not self.connection.is_connected:
            raise ConnectionError("Couldn't connect to the database")

        return self.connection

    def create_tables(self):
        cnx = self.get_connection()
        create_customer_statement = """
                CREATE TABLE IF NOT EXISTS customers (
                customerNumber INT PRIMARY KEY,
                customerName VARCHAR(255),
                contactLastName VARCHAR(255),
                contactFirstName VARCHAR(255),
                phone VARCHAR(15),
                addressLine1 VARCHAR(255),
                addressLine2 VARCHAR(255),
                city VARCHAR(255),
                state VARCHAR(255),
                postalCode VARCHAR(255),
                country VARCHAR(255),
                salesRepEmployeeNumber INT,
                creditLimit FLOAT
                );"""

        create_order_statement = """
                        CREATE TABLE IF NOT EXISTS orders (
                        orderNumber INT PRIMARY KEY,
                        orderDate DATE,
                        requiredDate DATE,
                        shippedDate DATE,
                        status VARCHAR(50),
                        comments VARCHAR(255),
                        customerNumber INT
                        );"""

        with cnx.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

            cursor.execute(f"USE {self.database}")

            cursor.execute(create_customer_statement)
            cursor.execute(create_order_statement)
            self.connection.commit()

    def insert_customer(self, customer):
        cnx = self.get_connection()

        insert_statement = """INSERT INTO customers (
                    customerNumber, customerName, contactLastName, contactFirstName,
                    phone, addressLine1, addressLine2, city, state,
                    postalCode, country, salesRepEmployeeNumber, creditLimit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ;"""

        with cnx.cursor() as cursor:
            cursor.execute(f"USE {self.database}")

            cursor.execute(insert_statement, customer)
            cnx.commit()
        return {
            "status": "success",
        }

    def insert_order(self, order):
        cnx = self.get_connection()

        insert_statement = """INSERT INTO orders (
                    orderNumber, CAST(orderDate AS DATE), CAST(requiredDate AS DATE),
                    CAST(shippedDate AS DATE), status, comments, customerNumber)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ;"""

        with cnx.cursor() as cursor:
            cursor.execute(f"USE {self.database}")

            cursor.execute(insert_statement, order)
            cnx.commit()
        return {
            "status": "success",
        }
