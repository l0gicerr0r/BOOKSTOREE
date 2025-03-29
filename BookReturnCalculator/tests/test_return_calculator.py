import unittest
from book_return_pkg.return_calculator import BookReturnCalculator
from datetime import datetime, timedelta

class TestBookReturnCalculator(unittest.TestCase):
    def test_calculate_due_date(self):
        calculator = BookReturnCalculator(7)  # 7-day borrowing period
        borrow_date = "2025-03-17"
        expected_due_date = (datetime.strptime(borrow_date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        
        self.assertEqual(calculator.calculate_due_date(borrow_date), expected_due_date)

    def test_is_overdue(self):
        calculator = BookReturnCalculator()
        past_due_date = "2024-03-10 12:00:00"  # A past date
        
        self.assertTrue(calculator.is_overdue(past_due_date))

if __name__ == '__main__':
    unittest.main()
