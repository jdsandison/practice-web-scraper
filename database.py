import mysql.connector


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Southampton1!"
    )
    mycursor = mydb.cursor()
    mycursor.execute("USE webscraper")
    mycursor.execute("SELECT * FROM manufacturers WHERE manufacturer_name = 'jaguar'")
    for x in mycursor:
        print(x)

    mycursor.execute("DESCRIBE data")
    for x in mycursor:
        print(x)

if __name__ == "__main__":
    main()
