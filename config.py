import pymysql

TOKEN = '6549927354:AAG7s0Urf9K5KJU0O5IEl74sTrV9NuPZSpM'

connection = pymysql.connect(
    host='roundhouse.proxy.rlwy.net',
    port=13374,
    user='root',
    password='GA4AFEgDgGbaaaEBgA-GGaDB6fdeHbbD',
    database='railway'
)

# connection = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='childs'
# )

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id int AUTO_INCREMENT, name varchar(100), presence varchar(1), status varchar(1), PRIMARY KEY (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS chats (id int AUTO_INCREMENT, username varchar(100), _id int(10), PRIMARY KEY (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS ready (id int AUTO_INCREMENT, name varchar(100), status varchar(1), PRIMARY KEY (id))")
