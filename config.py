import pymysql

TOKEN = '6501337482:AAGQPejyBdZLl27c1W7XPQKjDBmHw7e6TI8'

connection = pymysql.connect(
    host='mysql://children-user:HaDQ1xA8vW3j@srv-captain--crmojtdafy-mysql-80x:3306/children-database',
    user='children-user',
    password='HaDQ1xA8vW3j',
    database='children-database'
)

cursor = connection.cursor()
