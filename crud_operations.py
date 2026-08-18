from expense import Expense


class ExpenseOperations:

    def __init__(self, db):
        self.db = db

    def add_expense(self, expense, user_id):
        cursor = self.db.db.cursor()

        try:
            query = "insert into expenses (user_id, date, category, amount, description) values (%s, %s, %s, %s, %s)"

            cursor.execute(query, (
                user_id,
                expense.date,
                expense.category,
                expense.amount,
                expense.description
            ))

            self.db.db.commit()

            expense.id = cursor.lastrowid

            return True, "expense added successfully"

        except:
            self.db.db.rollback()
            return False, "error adding expense"

        finally:
            cursor.close()


    def get_all_expenses(self, user_id):
        cursor = self.db.db.cursor()

        try:
            query = "select id, date, category, amount, description, created_at from expenses where user_id = %s order by date desc"

            cursor.execute(query, (user_id,))

            return cursor.fetchall()
        
        except:
            self.db.db.rollback()
            return False, "error getting expenses"

        finally:
            cursor.close()


    def get_expense(self, expense_id, user_id):
        cursor = self.db.db.cursor()

        try:
            query = "select id, date, category, amount, description, created_at from expenses where id = %s and user_id = %s"

            cursor.execute(query, (expense_id, user_id))

            return cursor.fetchone()

        except:
            self.db.db.rollback()
            return False, "error getting expense"

        finally:
            cursor.close()

    def update_expense(self, expense, user_id):
        cursor = self.db.db.cursor()

        try:
            query = "update expenses set date = %s, category = %s, amount = %s, description = %s where id = %s and user_id = %s"

            cursor.execute(query, (
                expense.date,
                expense.category,
                expense.amount,
                expense.description,
                expense.id,
                user_id
            ))

            self.db.db.commit()

            return True, "expense updated successfully"

        except:
            self.db.db.rollback()
            return False, "error updating expense"

        finally:
            cursor.close()

    def delete_expense(self, expense_id, user_id):
        cursor = self.db.db.cursor()

        try:
            query = " delete from expenses where id = %s and user_id = %s"

            cursor.execute(query, (expense_id, user_id))

            self.db.db.commit()

            return True, "expense deleted successfully"

        except:
            self.db.db.rollback()
            return False, "Error deleting expense"

        finally:
            cursor.close()