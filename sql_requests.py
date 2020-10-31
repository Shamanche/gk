import pyodbc

def mssql_connect():
    driver = 'DRIVER={ODBC Driver 17 for SQl Server}'
    server = 'SERVER=test.gorkarta.ru'
    port = 'PORT=1433'
    db = 'DATABASE=RSLoyalty5'
    user = 'UID=sa'
    pw = 'PWD=Hymp112'
    conn_str = ';'.join([driver, server, port, db, user, pw])
    print(conn_str)
    conn = pyodbc.connect(conn_str, timeout=1)
    return conn

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
    sql_request ="exec get_phones {}, '{}', '{}'".format(company_id,
                                                        first_date, last_date)
    sql_request = "exec get_phones 4, '20130101', '20131231'"
    print(sql_request)
    print('firstdate: ', first_date, type(first_date))
    print('lastdate', last_date)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

conn = mssql_connect()
cursor = conn.cursor()
script = """
    select distinct	CustomerPhones.Phone
    from Transactions, Stores, Companies, DiscountCards, Accounts, CustomerPhones
    where Transactions.StoreID = Stores.StoreID
    	and Stores.CompanyID = Companies.CompanyID
    	and Companies.CompanyID = 74
    	and Transactions.DiscountCardID = DiscountCards.DiscountCardID
    	and DiscountCards.AccountID = Accounts.AccountID
    	and Accounts.CustomerID = CustomerPhones.CustomerID"""

