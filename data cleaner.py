import pandas as pd


def remove_rows_with_unavailable_price_and_long_company(file_path, sheet_to_skip='none'):
    # Read all sheets into a dictionary of DataFrames
    all_sheets = pd.read_excel(file_path, sheet_name=None)

    # Remove rows with 'Price unavailable'
    for sheet_name, df in all_sheets.items():
        if sheet_name != sheet_to_skip:
            all_sheets[sheet_name] = df[df['price'] != 'Price unavailable']

    # Remove rows with 'company' entry size more than 50 characters
    for sheet_name, df in all_sheets.items():
        all_sheets[sheet_name] = df[df['company'].apply(lambda x: len(str(x)) <= 50)]

    # Save the modified DataFrames back to the Excel file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)


file_path = 'C:\\Users\\saran\\OneDrive\\Desktop\\flight\\google_flights_data.xlsx'
sheet_to_skip = 'none'

try:
    remove_rows_with_unavailable_price_and_long_company(file_path, sheet_to_skip)
    print(f"Rows with 'Price unavailable' and 'company' entry size more than 50 characters removed from {file_path}, skipped sheet: {sheet_to_skip}")
except Exception as e:
    print(f"An error occurred: {e}")
