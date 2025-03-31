from datetime import datetime, timedelta

class BookReturnCalculator:
    """A library to calculate book return due dates and check for overdue books."""

    def __init__(self, borrow_period_days=14):
        """
        Initialize with a default borrowing period (default: 14 days).
        
        :param borrow_period_days: Number of days before the book is due.
        """
        self.borrow_period_days = borrow_period_days

    def calculate_due_date(self, borrow_date=None):
        """
        Calculate the return due date based on the borrowing date.

        :param borrow_date: Date the book was borrowed (format: YYYY-MM-DD).
                            If None, today's date is used.
        :return: Due date in "YYYY-MM-DD HH:MM:SS" format.
        """
        if borrow_date is None:
            borrow_date = datetime.utcnow()
        else:
            borrow_date = datetime.strptime(borrow_date, "%Y-%m-%d")

        due_date = borrow_date + timedelta(days=self.borrow_period_days)
        return due_date.strftime("%Y-%m-%d %H:%M:%S")

    def is_overdue(self, due_date):
        """
        Check if a book is overdue.

        :param due_date: Return due date (format: YYYY-MM-DD HH:MM:SS).
        :return: True if overdue, False otherwise.
        """
        due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
        return datetime.utcnow() > due_date
