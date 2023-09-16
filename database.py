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

    fuel_name = ""
    manufacturer = ""
    fuel_type_id = 0
    body_type_id = 0
    model_id = 0
    manufacturer_id = 0
    row = 0
    column_fuel = 5
    column_body_types = 8

    number_of_rows = len(file['ID value'])
    for row in range(number_of_rows):
        # the following is to split the makes_and_models column into separate makes and models columns
        model = ""
        make_and_model = file.iat[row, 0]
        # this is to catch the exceptions to brands with a space in the name
        if make_and_model.split(' ', 1) == 'Land' or 'Aston' or 'Alfa':
            manufacturer = make_and_model.split(' ', 2)[0]
            for i in range(len(make_and_model.split(' ', 2))-1):
                model = model + ' ' + make_and_model.split(' ', 2)[i+1]
                model = model.lstrip()

        else:
            manufacturer = make_and_model.split(' ', 1)[0]
            for i in range(len(make_and_model.split(' ', 2))-1):
                model = model + ' ' + make_and_model.split(' ', 2)[i+1]
                model = model.lstrip()

        mycursor.execute("SELECT * FROM manufacturers WHERE manufacturer_name = '" + manufacturer + "' LIMIT 1")
        record_manufacturer = mycursor.fetchone()
        if record_manufacturer is None:
            statement_manufacturer = "INSERT INTO `webscraper`.`manufacturers` (manufacturer_name) VALUES ('" + manufacturer +"');"
            mycursor.execute(statement_manufacturer)
            manufacturer_id = mycursor.lastrowid

        else:
            manufacturer_id = record_manufacturer[0]

        mycursor.execute("SELECT * FROM models WHERE model_name = '" + model + "' LIMIT 1")
        record_model = mycursor.fetchone()
        if record_model is None:
            statement_model = "INSERT INTO `webscraper`.`models` (`model_name`) VALUES ('" + model + "');"
            mycursor.execute(statement_model)
            model_id = mycursor.lastrowid

        else:
            model_id = record_model[0]

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
        record_body = mycursor.fetchone()

        if record_body is None:
            statement = "INSERT INTO `webscraper`.`body_types` (`body_type`) VALUES ('" + body_type_name + "');"
            mycursor.execute(statement)
            body_type_id = mycursor.lastrowid

        else:
            body_type_id = record_body[0]

        final_statement = "INSERT INTO `webscraper`.`dataset` (manufacturer_id, model_id ,fuel_type_id, body_type_id) VALUES (" + str(manufacturer_id) + "," + str(model_id) + ","+ str(fuel_type_id) +"," + str(body_type_id) + ")"
        mycursor.execute(final_statement)


if __name__ == "__main__":
    main()

