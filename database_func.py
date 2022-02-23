import sqlite3


def database_dialog(que, *inf):
    connection = sqlite3.connect('coffees.db')
    cursor = connection.cursor()
    information = cursor.execute(que, inf).fetchall()
    connection.commit()
    connection.close()
    return information


def insert_new_coffee(name, degree_of_roast, ground_in_grains,
                      description, price, volume):
    database_dialog("""INSERT INTO coffees('sort_name', 'degree of roast', 'ground/in grains',
                        'taste description', 'price', 'packing volume') 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                    name, degree_of_roast, ground_in_grains,
                    description, price, volume)


def all_inf():
    return database_dialog("""SELECT * FROM coffees""")


def get_from_coffees_using_id(coffee_id):
    return database_dialog("""SELECT * FROM coffees WHERE ID == ?""", coffee_id)[0]


def change_coffee(name, degree_of_roast, ground_in_grains,
                  description, price, volume, i_d):
    database_dialog("""UPDATE coffees SET 'sort_name' = ?, 'degree of roast' = ?,
                        'ground/in grains' = ?, 'taste description' = ?,
                        'price' = ?, 'packing volume' = ? WHERE coffees.ID == ?""",
                    name, degree_of_roast, ground_in_grains,
                    description, price, volume, i_d)
