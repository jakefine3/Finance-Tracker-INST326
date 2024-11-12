import json
import sys
import requests

"""
Financial Management System
"""

class Finances:
    """
    Creates a class that holds the user's financial data.
    """
    
    def __init__(self):
        """
        Initializes user's finances
        
        Args:
            income: list of income sources
            expenses: list of expenses
            savings: list of different investments/savings accounts, etc.
        """
        self.income = []
        self.expenses = []
        self.transactions = []
        self.investments = {}
        
    def add_income(self, source, amount, date):
        """
        Adds a new income source to the system
        
        Args:
            source (str): represents the name of the income source(job, etc.)
            amount (float): $ amount of the income source
            date (str): date associated with the income source
        """
        self.income.append({'source': source, 'amount': amount, 'date': date})
            
    def add_expense(self, category, amount, date):
        """
        Adds a new expense category to the system
        
        Args:
            category (str): represents the name of the expense category
            amount (float): monetary amount of the expense category
            date (str): date associated with the expense category
        """
        self.expenses.append({'category': category, 'amount': amount, 'date': date})
            
    def add_transaction(self, date, category, amount, description):
        """
        Adds a new transaction to the system
        
        Args:
            date (str): date of the transaction
            category (str): category of the transaction (income, expense, savings)
            amount (float): monetary amount of the transaction
            description (str): description of the transaction
        """
        self.transactions.append({'date': date, 'category': category, 'amount': amount, 'description': description})
        
    def add_investment(self, asset, amount):
        """
        Adds a new asset/investment to the portfolio
        
        Args:
            asset (str): name of the asset
            amount (float): monetary cost of the asset
        """
        self.investments[asset] = amount
        
    def build_report(self, start_date, end_date):
        """
        Generates a report for the specified start and end dates
        
        Args:
            start_date (str): start date of reporting period
            end_date (str): end date of reporting period

        Returns:
        Comes back with a generate report from the beginning to end.
        """
        report = {
            'Income': [inc for inc in self.income if start_date <= inc['date'] <= end_date],
            'Expenses': [exp for exp in self.expenses if start_date <= exp['date'] <= end_date],
            'Transactions': [tra for tra in self.transactions if start_date <= tra['date'] <= end_date],
            'Investments': self.investments
        }
        
        return report

    #If we use a JSON for the data, this is how we would save the data to a JSON file
    def save_to_file(self, file_name):
        """
        Saves the financial data to a JSON file.

        Args:
            file_name (str): file that the data will be saved to.
        """        
        
        try:
            with open(file_name, 'w') as file:
                json.dump({'income': self.income, 'expenses': self.expenses}, file)
            print("Data saved.")
        except Exception as e:
            print(f"An error occurred while saving: {e}")

    #If we use a JSON for the financial data, this will read it and update the classes 
    def load_from_file(self, file_name):
        """
        Loads financial data from a JSON file and updates the class attributes.

        Args:
            file_name (str): file that the data will be saved to.
        """
        
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
                if 'income' in data:
                    self.income = data['income']
                if 'expenses' in data:
                    self.expenses = data['expenses']
                if 'transactions' in data:
                    self.transactions = data['transactions']
                if 'investments' in data:
                    for inv in data['investments']:
                        self.investments[inv['asset']] = inv['amount']
            print("Data loaded.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")

class Investments:
    """
    Represents the user's investments
    """
    
    def __init__(self, name):
        """
        Initializes the portfolio with an empty list and name
        
        Args:
            name (str): name of the portfolio
        """
        self.name = name
        self.investments = {} 
        
    def add_investment(self, asset, amount):
        """
        Adds a new asset/investment to the portfolio
        
        Args:
            asset (str): name of the asset
            amount (int): monetary cost of the asset
        """
        self.investments[asset] = amount
        
    def remove_investment(self, asset):
        """
        Removes an asset/investment from the portfolio
        
        Args:
            asset (str): name of the asset that's being removed
        """
        if asset in self.investments:
            del self.investments[asset]

    def calculate_investment_growth(self, asset, growth_rate):
        """
        Calculates the growth of an investment
        
        Args:
            asset (str): name of the asset
            growth_rate (float): rate of growth (e.g., 0.05 for 5% growth)
            
        Returns:
            float: updated investment amount after growth
        """
        if asset in self.investments:
            self.investments[asset] *= (1 + growth_rate)
            return self.investments[asset]
        else:
            print("Investment not found.")
            return None

def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount from one currency to another using the exchange rates from an external API.

    Args:
        amount (float): The amount to be converted.
        from_currency (str): The source currency code.
        to_currency (str): The target currency code.

    Returns:
        float: The converted amount if successful, None if an error occurs.

    Raises:
        Exception: If there's an issue with the API request or the currency codes, raises an invalidation in the input.
    """
    
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        #checks if from_currency and to_currency exists in the exchange rates data
        if from_currency not in data['rates']:
            raise Exception(f"Currency code '{from_currency}' not found. Please use a valid currency code.")

        rates = data['rates']

        if to_currency not in rates:
            raise Exception(f"Currency code '{to_currency}' not found. Please use a valid currency code.")

        return amount * rates[to_currency]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    """
    Runs the Financial Management System.
    """
    print("Welcome to the Financial Management System!")
    
    finances = Finances()
    investments = Investments("My Portfolio")
    
    while True:
        print("\nOptions:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Transaction")
        print("4. Add Investment")
        print("5. Generate Report")
        print("6. Save Data to JSON")
        print("7. Load Data from JSON")
        print("8. Convert Currency")
        print("9. View Income")
        print("10. View Expenses")
        print("11. View Transactions")
        print("12. View Investments")
        print("13. View Investment Growth")
        print("14. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            source = input("Enter the name of the income source: ")
            amount = float(input("Enter the $ from this income source: "))
            date = input("Enter the date this occurred (YYYY-MM-DD): ")
            finances.add_income(source, amount, date)
            print("Income added successfully.")
        elif choice == '2':
            category = input("Enter the name of the expense category: ")
            amount = float(input("Enter the cost ($) of this expense: "))
            date = input("Enter the date this occurred (YYYY-MM-DD): ")
            finances.add_expense(category, amount, date)
            print("Expense category added successfully.")
        elif choice == '3':
            date = input("Enter the date of the transaction (YYYY-MM-DD): ")
            category = input("Enter the category of the transaction (income/expense/savings): ")
            amount = float(input("Enter the amount of the transaction: "))
            description = input("Enter a description of the transaction: ")
            finances.add_transaction(date, category, amount, description)
            print("Transaction added successfully.")
        elif choice == '4':
            asset = input("Enter the name of the asset: ")
            amount = float(input("Enter the amount of the investment: "))
            investments.add_investment(asset, amount)
            print("Investment added successfully.")
        elif choice == '5':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            report = finances.build_report(start_date, end_date)
            print("Report:")
            print(report)
        elif choice == '6':
            file_name = input("Enter the file name to save data to: ")
            finances.save_to_file(file_name)
        elif choice == '7':
            file_name = input("Enter the file name to load data from: ")
            finances.load_from_file(file_name)
        elif choice == '8':
            amount = float(input("Enter the amount to convert: "))
            from_currency = input("Enter the source currency: ")
            to_currency = input("Enter the target currency: ")
            converted_amount = convert_currency(amount, from_currency, to_currency)
            if converted_amount is not None:
                print(f"Converted amount: {converted_amount} {to_currency}")
        elif choice == '9':
            print("Income:")
            for source in finances.income:
                print(f"Source: {source['source']}, Amount: {source['amount']}, Date: {source['date']}")
        elif choice == '10':
            print("Expenses:")
            for category in finances.expenses:
             print(f"Category: {category['category']}, Amount: {category['amount']}, Date: {category['date']}")
        elif choice == '11':
            print("Transactions:")
            for transaction in finances.transactions:
                print(f"Date: {transaction['date']}, Category: {transaction['category']}, Amount: {transaction['amount']}, Description: {transaction['description']}")
        elif choice == '12':
            print("Investments:")
            for asset, amount in finances.investments.items():
                print(f"Asset: {asset}, Amount: {amount}")
        elif choice == '13':
            asset = input("Enter the name of the asset: ")
            growth_rate = float(input ("Enter the growth rate (as a decimal): "))
            new_amount = investments.calculate_investment_growth(asset, growth_rate)
            if new_amount is not None:
                print(f"{asset}'s new value after growth: {new_amount}")
        elif choice == '14':
            print("Exiting Financial Management System.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
