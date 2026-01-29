import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILENAME = "expenses.csv"
FIELDNAMES = ["date", "category", "amount", "description"]

def add_expense():
    date_input = input("Enter date (DD-MM-YYYY): ")
    try:
        parsed_date = datetime.strptime(date_input, "%d-%m-%Y")
        formatted_date = parsed_date.strftime("%d-%m-%Y") 
    except ValueError:
        print("❌ Invalid date format! Please enter as DD-MM-YYYY.")
        return

    category = input("Enter category (Food, Travel, etc.): ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return

    description = input("Enter description: ")

    with open(FILENAME, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if os.stat(FILENAME).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "date": formatted_date,
            "category": category,
            "amount": amount,
            "description": description
        })

    print("✅ Expense added and saved to file!")
    
def show_expenses():
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        print("❌ No expenses recorded yet.")
        return

    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        print("\n📄 All Expenses:")
        for row in reader:
            print(f"{row['date']} | {row['category']} | ₹{row['amount']} | {row['description']}")
            
def show_expense_chart():
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        print("❌ No expenses recorded yet.")
        return

    category_totals = {}

    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            category = row["category"]
            amount = float(row["amount"])
            category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        print("❌ No data to show chart.")
        return

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("💸 Expense Breakdown by Category")
    plt.axis("equal")
    plt.show()

def monthly_report():
    if not os.path.exists(FILENAME) or os.stat(FILENAME).st_size == 0:
        print("❌ No expenses recorded yet.")
        return

    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    total = 0
    filtered_expenses = []

    with open(FILENAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                expense_date = datetime.strptime(row["date"], "%d-%m-%Y")
                if expense_date.month == int(month) and expense_date.year == int(year):
                    filtered_expenses.append(row)
                    total += float(row["amount"])
            except ValueError:
                print(f"⚠ Skipping invalid date format: {row['date']}")

    if filtered_expenses:
        print(f"\n📆 Expenses for {month}/{year}:")
        for row in filtered_expenses:
            print(f"{row['date']} | {row['category']} | ₹{row['amount']} | {row['description']}")
        print(f"\n🧾 Total Spent: ₹{total:.2f}")
    else:
        print(f"❌ No expenses found for {month}/{year}.")

def main():
    while True:
        print("\n📘 Personal Expense Tracker")
        print("1. Add Expense")
        print("2. Show All Expenses")
        print("3. Show Expense Chart 📊")
        print("4. Monthly Report 📅")
        print("5. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_expense_chart()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ✅ Entry point
if __name__ == "__main__":
    main()

