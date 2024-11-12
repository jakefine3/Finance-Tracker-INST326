import unittest
import Finance_Tracker

class TestFinanceMethods(unittest.TestCase):
    def setUp(self):
        """Setup for each test case; ensures each test is independent."""
        self.finances = Finance_Tracker.Finances()
        self.investments = Finance_Tracker.Investments("My Portfolio")

    def test_add_income(self):
        """Test adding income and validate all properties."""
        self.finances.add_income("Work Salary", 2000, "2024-05-01")
        expected = {'source': "Work Salary", 'amount': 2000, 'date': "2024-05-01"}
        self.assertIn(expected, self.finances.income)
        self.assertEqual(len(self.finances.income), 1)  # Ensure only one record is added

    def test_add_expense(self):
        """Test adding expenses and check for correct insertion."""
        self.finances.add_expense("Rent", 1000, "2024-05-05")
        expected = {'category': "Rent", 'amount': 1000, 'date': "2024-05-05"}
        self.assertIn(expected, self.finances.expenses)
        self.assertEqual(len(self.finances.expenses), 1)  # Confirm one entry is present

    def test_add_transaction(self):
        """Ensure transactions are added correctly with all details."""
        self.finances.add_transaction("2024-05-10", "Expense", 50, "Groceries")
        expected = {'date': "2024-05-10", 'category': "Expense", 'amount': 50, 'description': "Groceries"}
        self.assertIn(expected, self.finances.transactions)
        self.assertEqual(self.finances.transactions[0]['amount'], 50)  # Verify amount

    def test_add_investment(self):
        """Test investment addition and assert correctness of the update."""
        self.investments.add_investment("Stocks", 5000)
        self.assertEqual(self.investments.investments.get("Stocks"), 5000)

    def test_remove_investment(self):
        """Check correct investment removal functionality."""
        self.investments.add_investment("Stocks", 5000)
        self.investments.remove_investment("Stocks")
        self.assertNotIn("Stocks", self.investments.investments)

    def test_calculate_investment_growth(self):
        """Test the calculation of investment growth."""
        self.investments.add_investment("Stocks", 5000)
        self.investments.calculate_investment_growth("Stocks", 0.10)  # 10% growth
        self.assertEqual(self.investments.investments["Stocks"], 5500)

    def test_build_report(self):
        """Verify that reports are generated correctly with accurate data."""
        self.finances.add_income("Work Salary", 2000, "2024-05-01")
        self.finances.add_expense("Rent", 1000, "2024-05-05")
        self.finances.add_transaction("2024-05-10", "Expense", 50, "Groceries")
        report = self.finances.build_report("2024-05-01", "2024-05-10")
        self.assertEqual(report['Income'][0], {'source': 'Work Salary', 'amount': 2000, 'date': '2024-05-01'})
        self.assertEqual(report['Expenses'][0], {'category': 'Rent', 'amount': 1000, 'date': '2024-05-05'})
        self.assertEqual(report['Transactions'][0], {'date': '2024-05-10', 'category': 'Expense', 'amount': 50, 'description': 'Groceries'})

    def test_save_to_file(self, mock_open):
        file_name = "test.json"
        self.finances.save_to_file(file_name)
        mock_open.assert_called_once_with(file_name, 'w')
        handle = mock_open()
        handle.write.assert_called_once_with('{"income": [{"source": "Work Salary", "amount": 2000, "date": "2024-05-01"}], "expenses": [{"category": "Rent", "amount": 1000, "date": "2024-05-05"}]}')
        print("Data saved.")

    def test_load_from_file(self, mock_open):
        file_name = "test.json"
        self.finances.load_from_file(file_name)
        self.assertEqual(len(self.finances.income), 1)
        self.assertEqual(len(self.finances.expenses), 1)
        self.assertEqual(self.finances.income[0], {'source': 'Work Salary', 'amount': 2000, 'date': '2024-05-01'})
        self.assertEqual(self.finances.expenses[0], {'category': 'Rent', 'amount': 1000, 'date': '2024-05-05'})
        print("Data loaded.")

    def test_convert_currency(self, mock_get):
        mock_response = {
            'rates': {
                'USD': 1.0,
                'EUR': 0.9,
                'GBP': 0.8
            }
        }
        mock_get.return_value.json.return_value = mock_response

        amount = 100
        from_currency = 'USD'
        to_currency = 'EUR'
        converted_amount = self.convert_currency(amount, from_currency, to_currency)

        expected_amount = amount * mock_response['rates'][to_currency]
        self.assertEqual(converted_amount, expected_amount)

    def test_main(self, mock_stdout, mock_input):
        mock_input.side_effect = ['1', 'Work Salary', '2000', '2024-05-01', '14']
        self.main()
        expected_output = (
            "Welcome to the Financial Management System!\n"
            "\nOptions:\n1. Add Income\n2. Add Expense\n3. Add Transaction\n4. Add Investment\n5. Generate Report\n6. Save Data to JSON\n7. Load Data from JSON\n8. Convert Currency\n9. View Income\n10. View Expenses\n11. View Transactions\n12. View Investments\n13. View Investment Growth\n14. Quit\n"
            "Income added successfully.\nExiting Financial Management System.\n"
        )
        self.assertEqual(mock_stdout.write.call_args[0][0], expected_output)
        
if __name__ == '__main__':
    unittest.main()
