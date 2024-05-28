import mysql.connector
import pandas as pd
import os
file = pd.read_csv(r'data.csv')
status_file = pd.read_csv(r'status-file.csv')
mysql_password = os.environ.get("MYSQL_PASSWORD")

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password
    )
mydb.autocommit = True
mycursor = mydb.cursor()
mycursor.execute("USE webscraper")
mycursor.execute("SELECT * FROM webscraper.dataset dt INNER JOIN webscraper.status s ON dt.advert_id = s.advert_id")

rows = mycursor.fetchall()

columns = [i[0] for i in mycursor.description]


df = pd.DataFrame(rows, columns=columns)
df = df.iloc[:, :-2].join(df.iloc[:, -1])

df.to_csv('data2.csv', index=False)