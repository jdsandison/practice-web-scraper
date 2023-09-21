import mysql.connector
import pandas as pd
import os
file = pd.read_csv(r'data.csv')
status_file = pd.read_csv(r'status-file.csv')
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
    colour_of_car = ""
    mpg = 0
    doors = 0
    seats = 0
    engine_power = 0
    top_speed = 0
    acceleration = 0
    co2 = 0
    tank_range = 0
    status = ""
    price = ""

    row = 0
    column_fuel = 5
    column_body_types = 8

    truncate_dataset = "TRUNCATE `webscraper`.`dataset`"
    truncate_status = "TRUNCATE `webscraper`.`status`"
    mycursor.execute(truncate_dataset)
    mycursor.execute(truncate_status)


    number_of_rows = len(file['ID value'])
    for row in range(number_of_rows):
        print(row)

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
            transmission_id = mycursor.lastrowid
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
        id_value = file.iat[row, 1]
        year = file.iat[row, 2]
        engine_size = file.iat[row, 3]
        mileage = file.iat[row, 4]
        colour_of_car = file.iat[row, 7]
        mpg = file.iat[row, 9]
        doors = file.iat[row, 11]
        seats = file.iat[row, 12]
        engine_power = file.iat[row, 13]
        top_speed = file.iat[row, 14]
        acceleration = file.iat[row, 15]
        co2 = file.iat[row, 16]
        tank_range = file.iat[row, 17]

        if ',' in tank_range:
            tank_range = tank_range.replace(',', '')

        mileage = mileage.replace(",", "")
        mileage = int(mileage)

        price = status_file.iat[row, 2]
        price = price.replace(",", "")
        price = int(price)

        final_statement = "INSERT INTO `webscraper`.`dataset` (advert_id , Year , `Engine size (litres)`,`Mileage (miles)`, Colour, fuel_type_id, transmission_type_id, body_type_id, manufacturer_id, model_id, Mpg, wheel_drive_type_id, Doors, Seats, `Engine power (bhp)`, `Top speed (mph)`, `Acceleration (0-62 mph) (seconds)`, `CO2 rating (g/km)`, `Tank range (miles)`, price) VALUES (" + str(id_value) + "," + str(year) + "," + str(engine_size) + ","+ str(mileage) + ",'" + colour_of_car + "'," + str(fuel_type_id) + "," + str(transmission_id) + "," + str(body_type_id) + "," + str(manufacturer_id) + "," + str(model_id) + "," + str(mpg) + "," + str(wheel_drive_id) + "," + str(doors) + "," + str(seats) + "," + str(engine_power) + "," + str(top_speed) + "," + str(acceleration) + "," + str(co2) + "," + str(tank_range) + "," + str(price) +")"

        list2 = [id_value, year, engine_size, mileage, colour_of_car, mpg, doors, seats, engine_power, top_speed, acceleration, co2, tank_range, price]
        print(id_value, year, engine_size, mileage, colour_of_car, mpg, doors, seats, engine_power, top_speed, acceleration, co2, tank_range, price, len(list2))

        mycursor.execute(final_statement)


        # status-file data:
        if status_file.iat[row, 1] == 'still active':
            status = None
        else:
            status = status_file.iat[row, 1]

        status_statement = "INSERT INTO `webscraper`.`status` (advert_id, status) VALUES (" + str(id_value) + "," + ("'" + str(status) + "'" if status is not None else "NULL") + ")"
        mycursor.execute(status_statement)

    rover_statement = "UPDATE models SET model_name = SUBSTRING_INDEX(model_name, ' ', -1) WHERE model_name LIKE 'Rover%'"
    mycursor.execute(rover_statement)

    # joining the two tables and printing the result
    query = "SELECT dataset.*, status.status FROM dataset LEFT JOIN status ON dataset.advert_id = status.advert_id"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()

