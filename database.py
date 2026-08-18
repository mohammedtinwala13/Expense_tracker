# this file handles all the database operations for the program

import MySQLdb as sql


class DataBase:

    # initializes the database config.
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db = None
        self.cursor = None

    def connect(self):

        #tries connecting sql with data provided
        try:
            self.db = sql.connect(
                self.host,
                self.user,
                self.password,
                self.database
                )
            self.cursor = self.db.cursor()
            print("\nSQL successfully connected")

        #accepts error and prints approriate error message
        except sql.Error as e:

            if e.args[0] == 2005: #error id 2005
                print("\nunknown server host")

            elif e.args[0] == 1045: #error id 1045
                print("\nusername and password dont match")

            elif e.args[0] == 1049: #error id 1049
                print("\nunknown database mentioned")

            elif e.args[0] == 2002: #error id 2002
                print("\ncannot connect to database, check if running")

            else: # for other general errors
                print(e.args)
            

    def disconnect(self):
        try:
            self.db.close()
            print("\ndatabase closed successfully")
            
        except:
            print("\ndatabase not activated")

    def is_connected(self):
        try:
            self.db.ping()
            print("\ndatabase active")
            return True
        except sql.Error as e:
            print(f"Database connection error,   {e}")
            return False

    def if_exists(self, table_name):
        query = f"SHOW TABLES LIKE '"+ table_name +"' "
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response == None:
            print("no table found in database, please create first")
        else:
            print(table_name,"table found in database, proceeding with query")



    def create_table_expenses(self):

        if not self.is_connected():
            return

        query = "create table if not exists expenses (" \
        "id int auto_increment primary key," \
        "user_id int not null," \
        "date date not null," \
        "category varchar(50) not null," \
        "amount decimal(10,2) not null," \
        "description varchar(150)," \
        "created_at timestamp default current_timestamp," \
        "FOREIGN KEY (user_id) REFERENCES users(id)" \
        ")"
        try:
            self.cursor.execute(query)
            self.db.commit()
            print("\n expenses table created in database")
        except sql.Error as e:
                print(f"table creation error,   {e}")
                return False


    def create_table_users(self):

        if not self.is_connected():
            return

        query = "create table if not exists users (" \
        "id int auto_increment primary key," \
        "username varchar(50) not null," \
        "password varchar(50) not null," \
        "name varchar(50) not null," \
        "created_at timestamp default current_timestamp" \
        ")"
        try:
            self.cursor.execute(query)
            self.db.commit()
            print("\n users table created in database")
        except sql.Error as e:
                print(f"table creation error,   {e}")
                return False
        
        





# obj1 = DataBase("localhost","root","MYSQL@123","python")
# obj1.connect()
# obj1.create_table_users()
# obj1.create_table_expenses()
# # obj1.disconnect()
# obj1.if_exists("expenses")
# obj1.if_exists("users")