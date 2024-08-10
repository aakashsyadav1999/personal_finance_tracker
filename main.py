import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
import warnings
warnings.filterwarnings('ignore')

class CSV:
    
    CSV_FILE = 'finance_data.csv'
    
    @classmethod
    def initialize(cls):
        try:
            if not os.path.exists(cls.CSV_FILE):
                cls.create_csv()
        except Exception as e:
            print(f"Error in opening file {e}")

    @classmethod
    def create_csv(cls):
        try:
            if not os.path.exists(cls.CSV_FILE):
                print(f"Creating {cls.CSV_FILE}")
                pd.DataFrame(columns=['date','amount','category','description']).to_csv(cls.CSV_FILE, index=False)
            elif os.path.exists(cls.CSV_FILE):
                print(f"File {cls.CSV_FILE} already exists")
        except Exception as e:
            print(f"Error in creating file {e}")
    
    @classmethod    
    def read_csv(cls):
        df = pd.read_csv(cls.CSV_FILE)
        return df
    
    @classmethod
    def insert_data(cls, date, amount, category, description):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            new_data = pd.DataFrame([{
                'date': date,
                'amount': amount,
                'category': category,
                'description': description
            }])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(cls.CSV_FILE, index=False)
        except Exception as e:
            print(f"Error in inserting data: {e}")
    
    @classmethod
    def create_pie_chart(cls):
        df = pd.read_csv(cls.CSV_FILE)
        df = df.groupby('category')['amount'].sum()
        df.plot(kind='pie',autopct='%1.1f%%')
        plt.show()
    
    @classmethod
    def line_chart(cls):
        df = pd.read_csv(cls.CSV_FILE)
        df = df.groupby(['date','category'])['amount'].sum()
        df.plot(kind='line')
        plt.show()
    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        filter_data = df.loc[mask]
        
        if filter_data.empty:
            print("No transactions found for the given date range")
        else:
            print(f"Transactions from {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}")
            
            print(
                filter_data.to_string(
                    index=False, 
                    formatters={"date": lambda x: x.strftime('%d-%m-%Y')}
                )
            )
            
            total_income = filter_data[filter_data["category"] == 'Income']['amount'].sum()
            total_expense = filter_data[filter_data["category"] == 'Expense']['amount'].sum()
            print("\nSummary")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net: ${total_income - total_expense:.2f}")


def add_data():
    CSV.initialize()
    date = get_date(
                    "Enter the date (DD-MM-YYYY) or enter for today's date: ", 
                    allow_default=True
                    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.insert_data(date,amount,category,description)

CSV.get_transactions('14-07-2024','11-08-2024')
#add_data()




