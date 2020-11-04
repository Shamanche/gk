import pymysql, pymssql
##import pyodbc

def mysql_connect():
    conn = pymysql.connect(host='test.gorkarta.ru',
                           user='root',
                           password='Sm620514',
                           db='Ccserver')
    return conn

def mssql_connect():
    conn = pymssql.connect(
        server="test.gorkarta.ru",
        database="RSLoyalty5",
        user="sa",
        password="Hymp112",
        port=1433)
    return conn


##def mssql_connect():
##    driver = 'DRIVER={ODBC Driver 17 for SQl Server}'
##    server = 'SERVER=test.gorkarta.ru'
##    port = 'PORT=1433'
##    db = 'DATABASE=RSLoyalty5'
##    user = 'UID=sa'
##    pw = 'PWD=Hymp112'
##    conn_str = ';'.join([driver, server, port, db, user, pw])
##    print(conn_str)
##    conn = pyodbc.connect(conn_str, timeout=1)
##    return conn

def count_transactions(conn):
    sql_request ="select count(*) FROM Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    return row[0]

def first_transaction(conn):
    sql_request ="select min(TransactionTime) from Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    print('first_transaction: ', row[0])
    return row[0]

def last_transaction(conn):
    sql_request ="select max(TransactionTime) from Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    print('last_transaction: ', row[0])
    return row[0]

def get_all_companies(conn):
    sql_request ="select CompanyID, Name from Companies"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

# у company_id=4 всего 25 телефонов
def get_mssql_phones (conn, company_id, first_date, last_date):
    print('Start get_mssql_phones ')
    sql_request ="""
        select distinct	CustomerPhones.Phone
        from Transactions, Stores, Companies, DiscountCards,
                                                        Accounts, CustomerPhones
        where Transactions.TransactionTime between '{}' and '{}'
    		and Transactions.StoreID = Stores.StoreID
        	and Stores.CompanyID = Companies.CompanyID
        	and Companies.CompanyID = {}
        	and Transactions.DiscountCardID = DiscountCards.DiscountCardID
        	and DiscountCards.AccountID = Accounts.AccountID
        	and Accounts.CustomerID = CustomerPhones.CustomerID
                """.format(first_date, last_date, company_id)
    print(sql_request)
    print('firstdate: ', first_date, type(first_date))
    print('lastdate', last_date)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

def get_mysql_phones(conn):
    print('Start get_MYSQL_phones ')
    sql_request = "SELECT phone FROM user WHERE token IS NOT NULL"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

##conn = mssql_connect()
##cursor = conn.cursor()
##script = """
##    select distinct	CustomerPhones.Phone
##    from Transactions, Stores, Companies, DiscountCards, Accounts, CustomerPhones
##    where Transactions.TransactionTime between '2019-01-01' and '2019-31-12'
##		and Transactions.StoreID = Stores.StoreID
##    	and Stores.CompanyID = Companies.CompanyID
##    	and Companies.CompanyID = 74
##    	and Transactions.DiscountCardID = DiscountCards.DiscountCardID
##    	and DiscountCards.AccountID = Accounts.AccountID
##    	and Accounts.CustomerID = CustomerPhones.CustomerID"""

