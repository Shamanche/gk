import unittest, pymssql, datetime

CONN = pymssql.connect(
    server="test.gorkarta.ru",
    database="RSLoyalty5",
    user="sa",
    password="Hymp112",
    port=1433)


class SqlTestCase(unittest.TestCase):

    def test_first_transaction(self):
        sql ="select min(TransactionTime) from Transactions"
        cursor = CONN.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()[0][0]
        self.assertEqual(res, datetime.datetime(2012, 2, 3, 16, 43, 2))

if __name__ == '__main__':
    unittest.main()