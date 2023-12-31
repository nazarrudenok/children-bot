import pymysql

TOKEN = '6501337482:AAGQPejyBdZLl27c1W7XPQKjDBmHw7e6TI8'

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='childs'
)

cursor = connection.cursor()