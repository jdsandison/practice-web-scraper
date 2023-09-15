import mysql.connector
import pandas as pd
import os

file = pd.read_csv(r'data.csv')
mysql_password = os.environ.get("MYSQL_PASSWORD")


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=mysql_password
    )
    mycursor = mydb.cursor()
    mycursor.execute("USE webscraper")
    mycursor.execute("SELECT * FROM manufacturers WHERE manufacturer_name = 'jaguar'")
    for x in mycursor:
        print(x)

    mycursor.execute("DESCRIBE data")
    for x in mycursor:
        print(x)
    fuel_name = ""
    fuel_type_id = 0
    row = 0
    column = 5

    number_of_rows = len(file['ID value'])
    for row in range(number_of_rows):
        fuel_name = file.iat[row, column]
        mycursor.execute("SELECT * FROM fuel_types WHERE fuel_type = '" + fuel_name + "'")
        if mycursor.rowcount == 1:
            # fuel type exists get the id
            for x in mycursor:
                print(x[0])
                fuel_type_id = x[0]
        else:
            print('create this')
            for x in mycursor:
                print(x)
                # run an insert statement to create this fuel type fuel_name
                # set fuel_type_id by reading the inserted id

        # at this point, we have fuel_type_id, so insert a row into DATA with this fuel type ID.


if __name__ == "__main__":
    main()

