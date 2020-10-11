import pymssql


conn = pymssql.connect(
    server="test.gorkarta.ru",
    database="RSLoyalty5",
    user="sa",
    password="Hymp112",
    port=1433)

def count_transactions(conn=conn):
    sql_request ="select count(*) FROM Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    return row[0]

def first_transaction(conn = conn):
    sql_request ="select min(TransactionTime) from Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    print('first_transaction: ', row[0])
    return row[0]

def last_transaction(conn = conn):
    sql_request ="select max(TransactionTime) from Transactions"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    row = cursor.fetchone()
    print('last_transaction: ', row[0])
    return row[0]

def get_all_companies(conn = conn):
    sql_request ="select CompanyID, Name from Companies"
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

# у company_id=4 всего 25 телефонов
def get_mssql_phones (company_id, first_date, last_date, conn=conn):
    print('Start get_mssql_phones ')
    sql_request ="exec get_phones {}, '{}', '{}'".format(company_id,
                                                        first_date, last_date)
    #sql_request = "exec get_phones 4, '20130101', '20131231'"
    print(sql_request)
    print('firstdate: ', first_date, type(first_date))
    print('lasdate', last_date)
    cursor = conn.cursor()
    cursor.execute(sql_request)
    rows = cursor.fetchall()
    return rows

#Yx = get_mssql_phones(4, "'20130101'", "'20131231'")

