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
    body_type_id = 0
    row = 0
    column_fuel = 5
    column_body_types = 8

    number_of_rows = len(file['ID value'])
    for row in range(number_of_rows):
        fuel_name = file.iat[row, column_fuel]
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
            fuel_type_id = record[0]


        # at this point, we have fuel_type_id, so insert a row into DATA with this fuel type ID.
        #statement = "INSERT INTO `webscraper`.`dataset` (`Make and model`, fuel_type_id) VALUES ('" + file.iat[row, 0] +"'," + str(fuel_type_id) +")"
        #mycursor.execute(statement)

        body_type_name = file.iat[row, column_body_types]
        mycursor.execute("SELECT * FROM body_types WHERE body_type = '" + body_type_name + "' LIMIT 1")
        record2 = mycursor.fetchone()

        # if LIMIT is 1 then mycursor.rowcount is always 1? Therefore, we should see when record2 is not present?
        if record2 is None:
            statement = "INSERT INTO `webscraper`.`body_types` (`body_type`) VALUES ('" + body_type_name + "');"
            mycursor.execute(statement)
            body_type_id = mycursor.lastrowid

        else:
            body_type_id = record2[0]


        print('body type id: ' + str(body_type_id))

        statement2 = "INSERT INTO `webscraper`.`dataset` (`Make and model`, fuel_type_id, body_type_id) VALUES ('" + file.iat[row, 0] + "'," + str(fuel_type_id) +", " + str(body_type_id) + ")"
        mycursor.execute(statement2)
    # similarly with the body type column, include a table of id's with respective body tpes (coupe, hatchback ect)
    # then split the make and model column into makes, models. And then create a table of each that number them with respective ids.


if __name__ == "__main__":
    main()

