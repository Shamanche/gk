import pymysql

conn = pymysql.connect(host='test.gorkarta.ru',
                             user='root',
                             password='Sm620514',
                             db='Ccserver')

with conn.cursor() as cursor:
    sql_request = "SELECT phone FROM user WHERE token IS NOT NULL"
    cursor.execute(sql_request)
    result = cursor.fetchone()


##import pymssql
##conn = pymssql.connect(
##    server="test.gorkarta.ru",
##    database="RSLoyalty5",
##    user="sa",
##    password="Hymp112",
##    port=1433)
