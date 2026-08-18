# analytics.py

import matplotlib.pyplot as plt


class Analytics:

    def __init__(self, db):
        self.db = db

    def plot_monthly_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT YEAR(date), MONTH(date), SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY YEAR(date), MONTH(date)
            ORDER BY YEAR(date), MONTH(date)
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        months = []
        amounts = []

        for year, month, total in data:
            months.append(f"{year}-{month:02d}")
            amounts.append(float(total))

        plt.figure()
        plt.plot(months, amounts, marker="o")
        plt.title("Monthly Spending")
        plt.xlabel("Month")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_category_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        categories = []
        amounts = []

        for category, total in data:
            categories.append(category)
            amounts.append(float(total))

        plt.figure()
        plt.bar(categories, amounts)
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_monthly_category_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT YEAR(date), MONTH(date), category, SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY YEAR(date), MONTH(date), category
            ORDER BY YEAR(date), MONTH(date)
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        months = sorted(
            set(f"{row[0]}-{row[1]:02d}" for row in data)
        )

        categories = sorted(
            set(row[2] for row in data)
        )

        values = {}

        for year, month, category, total in data:
            month_name = f"{year}-{month:02d}"
            values[(month_name, category)] = float(total)

        bottom = [0] * len(months)

        plt.figure()

        for category in categories:
            amounts = [
                values.get((month, category), 0)
                for month in months
            ]

            plt.bar(
                months,
                amounts,
                bottom=bottom,
                label=category
            )

            bottom = [
                bottom[i] + amounts[i]
                for i in range(len(months))
            ]

        plt.title("Monthly Category Spending")
        plt.xlabel("Month")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_top_expenses(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT date, category, amount, description
            FROM expenses
            WHERE user_id = %s
            ORDER BY amount DESC
            LIMIT 5
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        labels = []
        amounts = []

        for expense_date, category, amount, description in data:
            labels.append(f"{category} - {expense_date}")
            amounts.append(float(amount))

        plt.figure()
        plt.barh(labels[::-1], amounts[::-1])
        plt.title("Top 5 Expenses")
        plt.xlabel("Amount (₹)")
        plt.tight_layout()
        plt.show()

    def plot_daily_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT date, SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY date
            ORDER BY date
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        dates = []
        amounts = []

        for expense_date, total in data:
            dates.append(str(expense_date))
            amounts.append(float(total))

        plt.figure()
        plt.plot(dates, amounts, marker="o")
        plt.title("Daily Spending")
        plt.xlabel("Date")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_weekday_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT DAYNAME(date), SUM(amount)
            FROM expenses
            WHERE user_id = %s
            GROUP BY DAYOFWEEK(date), DAYNAME(date)
            ORDER BY DAYOFWEEK(date)
        """

        cursor.execute(query, (user_id,))
        data = cursor.fetchall()
        cursor.close()

        days = []
        amounts = []

        for day, total in data:
            days.append(day)
            amounts.append(float(total))

        plt.figure()
        plt.bar(days, amounts)
        plt.title("Spending by Weekday")
        plt.xlabel("Day")
        plt.ylabel("Amount (₹)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def get_total_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT SUM(amount)
            FROM expenses
            WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result[0] else 0

    def get_average_spending(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT AVG(amount)
            FROM expenses
            WHERE user_id = %s
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        return result[0] if result[0] else 0

    def get_highest_expense(self, user_id):
        cursor = self.db.db.cursor()

        query = """
            SELECT id, date, category, amount, description
            FROM expenses
            WHERE user_id = %s
            ORDER BY amount DESC
            LIMIT 1
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()

        return result