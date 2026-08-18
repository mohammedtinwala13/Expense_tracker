# expense.py

from datetime import datetime, date


class Expense:

    categories = [
        "food",
        "transport",
        "entertainment",
        "shopping",
        "utilities",
        "household",
        "healthcare",
        "education",
        "insurance",
        "maintenance",
        "personal",
        "taxes",
        "travelling",
        "savings",
        "others"
    ]

    def __init__(self, date, category, amount, description=""):
        self.id = None
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.created_at = datetime.now()



    def validate(self):

        return (
            self.validate_date()
            and self.validate_category()
            and self.validate_amount()
        )

    
    def validate_date(self):

        if isinstance(self.date, date):
            return True

        try:
            self.date = datetime.strptime(
                self.date, "%Y-%m-%d"
            ).date()

        except (ValueError, TypeError):
            return False

        if self.date > date.today():
            return False

        return True

    def validate_category(self):

        if not isinstance(self.category, str):
            return False

        self.category = self.category.strip().lower()

        if self.category not in self.categories:
            return False

        return True

    def validate_amount(self):

        try:
            self.amount = float(self.amount)
        except (ValueError, TypeError):
            return False

        if self.amount <= 0:
            return False

        self.amount = round(self.amount, 2)

        return True


