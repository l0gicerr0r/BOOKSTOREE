from book_return_lib.book_return_pkg.return_calculator import BookReturnCalculator


# Create an instance of BookReturnCalculator
calculator = BookReturnCalculator()

# Use the class methods
borrow_date = "2025-03-17"
due_date = calculator.calculate_due_date(borrow_date)

print(f"Borrow Date: {borrow_date}")
print(f"Return Due Date: {due_date}")
print(f"Is Overdue? {calculator.is_overdue(due_date)}")
