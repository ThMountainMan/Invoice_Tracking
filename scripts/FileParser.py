# This Script is a helper to convert the currently existing EXCEL Invoice sheet
# into the new Database Structure

import pandas as pd

# Define the File Path for the csv
filePath = r'F:\Development\Projects\Temp\Invoices.csv'

# Read the CSV Data into Pandas Data Frame
invoice_data = pd.read_csv(filePath, delimiter=";", encoding="cp1252")

print(invoice_data.head())
