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
    mydb.autocommit = True
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
        mycursor.execute("SELECT * FROM fuel_types WHERE fuel_type = '" + fuel_name + "' LIMIT 1")
        record = mycursor.fetchone()

        if mycursor.rowcount != 1:
            # run an insert statement to create this fuel type fuel_name
            # set fuel_type_id by reading the inserted id

            statement = "INSERT INTO `webscraper`.`fuel_types` (`fuel_type`) VALUES ('" + fuel_name + "');"
            mycursor.execute(statement)
            fuel_type_id = mycursor.lastrowid

        else:
            # fuel type exists get the id
            print(record[0])
            # for x in record:
            #    print(x)
            fuel_type_id = record[0]
            #    print('bob' + fuel_type_id)


        # at this point, we have fuel_type_id, so insert a row into DATA with this fuel type ID.
        statement = "INSERT INTO `webscraper`.`dataset` (`Make and model`, fuel_type_id) VALUES ('" + file.iat[row, 0] +"'," + str(fuel_type_id) +")"
        mycursor.execute(statement)
if __name__ == "__main__":
    main()

