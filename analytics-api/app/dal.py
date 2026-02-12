from mysql_connection import DbConnection

CNX = DbConnection()


def select_many(query: str):
    cnx = CNX.get_connection()
    with cnx.cursor(dictionary=True) as cursor:
        cursor.execute(f"USE {CNX.database}")
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_top_customers_by_orders():
    select_statement = """SELECT c.customerNumber, c.customerName, COUNT(o.orderNumber) as count
    FROM customers c INNER JOIN orders o
    ON c.customerNumber = o.customerNumber
    GROUP BY c.customerNumber, c.customerName
    ORDER BY count
    LIMIT 10;
    """
    return select_many(select_statement)


def get_customers_without_orders():
    select_statement = """SELECT c.customerNumber, c.customerName, COUNT(o.orderNumber) as count
    FROM customers c LEFT JOIN orders o
    ON c.customerNumber = o.customerNumber
    GROUP BY c.customerNumber, c.customerName
    HAVING COUNT(o.orderNumber) = 0;
    """
    return select_many(select_statement)


def get_zero_credit_active_customers():
    select_statement = """SELECT c.customerNumber, c.customerName, c.creditLimit
        FROM customers c INNER JOIN orders o
        ON c.customerNumber = o.customerNumber
        WHERE c.creditLimit = 0.0
        GROUP BY c.customerNumber, c.customerName
        """
    return select_many(select_statement)
