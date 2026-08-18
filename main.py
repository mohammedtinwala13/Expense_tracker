

from database import DataBase
from auth import Auth
from expense import Expense
from crud_operations import ExpenseOperations
from analytics import Analytics

import os
from dotenv import load_dotenv


def main():

    # =========================
    # DATABASE
    # =========================
    load_dotenv()

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")

    db = DataBase(
        host,
        user,
        password,
        database
    )

    db.connect()

    db.create_table_users()
    db.create_table_expenses()
    db.if_exists("users")
    db.if_exists("expenses")


    if not db.is_connected():
        print("Unable to connect to database.")
        return

    # =========================
    # OBJECTS
    # =========================

    auth = Auth(db)
    expenses = ExpenseOperations(db)
    analytics = Analytics(db)

    print("\n================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("================================")

    # =========================
    # LOGIN / REGISTER
    # =========================

    while True:

        print("\n1. Login")
        print("2. Create Account")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":

            username = input("Username: ")
            password = input("Password: ")

            success, message, *user = auth.login_user(
                username,
                password
            )

            print(message)

            if success:
                print("user id retrieved = ", user)
                user_id = user[0]
                break

        elif choice == "2":

            username = input("Username: ")
            password = input("Password: ")
            name = input("Name: ")

            success, message = auth.register_user(
                username,
                password,
                name
            )

            print(message)

        elif choice == "3":

            db.disconnect()
            return

        else:
            print("Invalid choice.")

    # =========================
    # USER MENU
    # =========================

    while True:

        print("\n================================")
        print("             MENU")
        print("================================")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Expense")
        print("4. Update Expense")
        print("5. Delete Expense")
        print("6. Analytics")
        print("7. Current User")
        print("8. Logout")

        choice = input("Enter choice: ")

        # -------------------------
        # ADD EXPENSE
        # -------------------------

        if choice == "1":

            print("\nAvailable Categories:")

            for category in Expense.categories:
                print("-", category)

            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            amount = input("Amount: ")
            description = input("Description: ")

            try:
                expense = Expense(
                    date,
                    category,
                    amount,
                    description
                )

                if not expense.validate():
                    print("Invalid expense data.")
                    continue

                success, message = expenses.add_expense(
                    expense,
                    user_id
                )

                print(message)

            except ValueError as e:
                print("Error:", e)

        # -------------------------
        # VIEW ALL EXPENSES
        # -------------------------

        elif choice == "2":

            data = expenses.get_all_expenses(user_id)

            if not data:
                print("No expenses found.")
                continue

            print("\nID | Date | Category | Amount | Description")

            for expense in data:
                print(expense)

        # -------------------------
        # VIEW ONE EXPENSE
        # -------------------------

        elif choice == "3":

            expense_id = input("Enter expense ID: ")

            try:
                expense_id = int(expense_id)
            except ValueError:
                print("Invalid ID.")
                continue

            expense = expenses.get_expense(
                expense_id,
                user_id
            )

            if expense:
                print(expense)
            else:
                print("Expense not found.")

        # -------------------------
        # UPDATE EXPENSE
        # -------------------------

        elif choice == "4":

            expense_id = int(input("Enter expense ID: "))

            old = expenses.get_expense(expense_id, user_id)

            if not old:
                print("Expense not found.")
                continue

            date = input(f"Date [{old[1]}]: ") or old[1]
            category = input(f"Category [{old[2]}]: ") or old[2]
            amount = input(f"Amount [{old[3]}]: ") or old[3]
            description = input(f"Description [{old[4]}]: ") or old[4]

            expense = Expense(date, category, amount, description)
            expense.id = expense_id

            if not expense.validate():
                print("Invalid expense data.")
                continue

            success, message = expenses.update_expense(
                                expense, user_id
                                )

            print(message)
        # -------------------------
        # DELETE EXPENSE
        # -------------------------

        elif choice == "5":

            expense_id = input("Enter expense ID: ")

            try:
                expense_id = int(expense_id)
            except ValueError:
                print("Invalid ID.")
                continue

            success, message = expenses.delete_expense(
                expense_id,
                user_id
            )

            print(message)


        elif choice == "7":

            current_user,message = auth.current_user()

            print("User ID: ",current_user[0])
            print("Username: ",current_user[1])

            print(message)

        # -------------------------
        # ANALYTICS
        # -------------------------

        elif choice == "6":

            while True:

                print("\n========== ANALYTICS ==========")
                print("1. Monthly Spending")
                print("2. Category Spending")
                print("3. Monthly Category Spending")
                print("4. Top 5 Expenses")
                print("5. Daily Spending")
                print("6. Weekday Spending")
                print("7. Spending Summary")
                print("8. Back")

                analytics_choice = input("Enter choice: ")

                if analytics_choice == "1":
                    analytics.plot_monthly_spending(user_id)

                elif analytics_choice == "2":
                    analytics.plot_category_spending(user_id)

                elif analytics_choice == "3":
                    analytics.plot_monthly_category_spending(
                        user_id
                    )

                elif analytics_choice == "4":
                    analytics.plot_top_expenses(user_id)

                elif analytics_choice == "5":
                    analytics.plot_daily_spending(user_id)

                elif analytics_choice == "6":
                    analytics.plot_weekday_spending(user_id)

                elif analytics_choice == "7":

                    total = analytics.get_total_spending(
                        user_id
                    )

                    average = analytics.get_average_spending(
                        user_id
                    )

                    highest = analytics.get_highest_expense(
                        user_id
                    )

                    print("\n========== SUMMARY ==========")
                    print(f"Total Spending: ₹{total:.2f}")
                    print(f"Average Expense: ₹{average:.2f}")

                    if highest:
                        print(
                            f"Highest Expense: ₹{highest[3]}"
                        )
                        print(
                            f"Category: {highest[2]}"
                        )
                        print(
                            f"Description: {highest[4]}"
                        )
                    else:
                        print("No expenses found.")

                elif analytics_choice == "8":
                    break

                else:
                    print("Invalid choice.")

        # -------------------------
        # LOGOUT
        # -------------------------

        elif choice == "8":

            auth.logout()
            print("Logged out successfully.")

            break

        else:
            print("Invalid choice.")

    # =========================
    # CLOSE DATABASE
    # =========================

    db.disconnect()


if __name__ == "__main__":
    main()