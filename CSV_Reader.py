
import pandas as pd

def get_total_revenue(csv_file_path, date) -> str:
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Convert Sales Date column to datetime format
        df['Sales Date'] = pd.to_datetime(df['Sales Date'])

        # Filter rows by Sales Date
        filtered_rows = df[df['Sales Date'] <= date]

        # Calculate total revenue
        total_revenue = filtered_rows['Revenue'].sum()

        return total_revenue
    except Exception as e:
        return f'Error: {str(e)}'
    
