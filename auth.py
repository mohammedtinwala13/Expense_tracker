from database import DataBase
from datetime import datetime, date


class Auth:
    def __init__(self, db):
        self.db = db
        self.user = None

    def register_user(self, username, password, name):

        if username == None or password == None or name == None:
            return False,"please enter all the credentials to proceed"

        if len(password)<8:
            return False,"please enter a password longer than 8 characters"

        cursor = self.db.db.cursor()
        created_at = datetime.now()

        try:
            query = "select id from users where username = '"+ username +"'    "
            cursor.execute(query)

            

            if cursor.fetchone():
                return False,"username already taken, please use another one"

            query = "insert into users (username, password, name, created_at) values (%s, %s, %s, %s)"

            cursor.execute(
            query,
            (username, password, name, created_at)
        )
            self.db.db.commit()

            return True, "account created succesfully"

        except:
            self.db.db.rollback()
            return False,"user creation error, try again"

        finally:

            cursor.close()


    def login_user(self, username, password):

        cursor = self.db.db.cursor()

        try:
            query = "select id, username, password from users where username = %s"

            cursor.execute(query, (username,))

            self.user = cursor.fetchone()

            if not self.user:
                return False, "username not found"

            user_id = self.user[0]
            stored_password = self.user[2]

            if stored_password == password:
                return True, "username and password matched!",user_id

            return False, "password is invalid"

        except :
            print("login error")
            return False, "error occurred in retrieving data"

        finally:
            cursor.close()


    def logout(self):
        self.user = None
        return True, "logged out succesfully"


    def current_user(self):
        if self.user is not None:
            return self.user[:2], "\nuser id and username of current user retrieved"
        else:
            return self.user, "\nno user found currently"


            
            
