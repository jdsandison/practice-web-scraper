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

    # initialising variables
    fuel_name = ""
    manufacturer = ""
    fuel_type_id = 0
    body_type_id = 0
    model_id = 0
    manufacturer_id = 0
    transmission_id = 0
    wheel_drive_id = 0
    id_value = 0
    year = 0
    engine_size = 0
    mileage = 0
    colour = 0
    mpg = 0
    doors = 0
    seats = 0
    engine_power = 0
    top_speed = 0
    acceleration = 0
    co2 = 0
    tank_range = 0
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

        # transmission column of the dataset
        transmission_name = file.iat[row, 6]
        mycursor.execute("SELECT * FROM transmission_types WHERE transmission_type = '" + transmission_name + "' LIMIT 1")
        record_transmission = mycursor.fetchone()

        if record_transmission is None:
            statement = "INSERT INTO `webscraper`.`transmission_types` (`transmission_type`) VALUES ('" + transmission_name + "');"
            mycursor.execute(statement)
            transmisison_id = mycursor.lastrowid()

        else:
            transmission_id = record_transmission[0]

        # Wheel drive column of the dataset
        wheel_drive_name = file.iat[row, 10]
        mycursor.execute("SELECT * FROM wheel_drive WHERE wheel_drive_type = '" + wheel_drive_name + "' LIMIT 1")
        record_wheel = mycursor.fetchone()

        if record_wheel is None:
            statement = "INSERT INTO `webscraper`.`wheel_drive` (`wheel_drive_type`) VALUES ('" + wheel_drive_name + "');"
            mycursor.execute(statement)
            wheel_drive_id = mycursor.lastrowid

        else:
            wheel_drive_id = record_wheel[0]

        # inserting the rest of the data




        final_statement = "INSERT INTO `webscraper`.`dataset` (manufacturer_id, model_id ,fuel_type_id, body_type_id, transmission_type_id, wheel_drive_type_id) VALUES (" + str(manufacturer_id) + "," + str(model_id) + ","+ str(fuel_type_id) +"," + str(body_type_id) + "," + str(transmission_id) + "," + str(wheel_drive_id) + ")"
        mycursor.execute(final_statement)


if __name__ == "__main__":
    main()

