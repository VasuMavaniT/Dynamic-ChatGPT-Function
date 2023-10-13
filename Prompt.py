def prompt_template():
    sk_prompt = '''
    Note: "You have to assume parameters based on description and output. Use existing functions or create new functions." 

    [Goal]
    What are the total number of records in the dataset?
    CSV: price.csv
    Skill: CSV_Reader
    Column: brand
    [Output]
    {
        "description": "Function that returns the total number of the records in the csv file",
        "name": "get_total_records",
        "function": """
def get_total_records(csv_file_path: str) -> list:
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        records = df.shape[0]

        return records
    except Exception as e:
        return f'Error: {str(e)}'
    """,
        "library": ["import pandas as pd"],
        "parameters": {
            "csv_file_path": "price.csv"
        },
        "output_type": "int",
        "call": "get_total_records('price.csv')"
    }


    [Goal]
    What are different brands of the products in the dataset?
    CSV: price.csv
    Column: brand
    Skill: CSV_Reader
    [Output]
    {
        "description": "Function that returns the different brands of the products in the csv file",
        "name": "get_brands",
        "function": """
# Start of the function

def get_brands(csv_file_path) -> str:
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Get the different brands in the DataFrame
        brands = df['brand'].unique()

        return brands
    except Exception as e:
        return f'Error: {str(e)}'
    """,
        "library": ["import pandas as pd"],
        "parameters": {
            "csv_file_path": "price.csv"
        },
        "output_type": "list",
        "call": "get_brands('price.csv')"
    }


    [Goal]
        What is the price of a refrigerator with Brand whirlpool and Model H?
        CSV: price.csv
        Column: brand
        Skill: CSV_Reader
    [Output]
    {
        "description": "Function that returns the price of a refrigerator with a given brand and model",
        "name": "get_refrigerator_price",
        "function": """
def get_refrigerator_price(csv_file_path, brand, model) -> str:
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Filter rows by Brand and Model
        filtered_rows = df[(df['Brand'] == brand) & (df['Model'] == model)]

        # Get the price from the first row of the filtered result
        price = filtered_rows.iloc[0]['Price']

        return price
    except Exception as e:
        return f'Error: {str(e)}'
    """,
        "library": ["import pandas as pd"],
        "parameters": {
            "csv_file_path": "price.csv",
            "brand": "whirlpool",
            "model": "H"
        },
        "output_type": "float",
        "call": "get_refrigerator_price('price.csv', 'whirlpool', 'H')"
    }

    [Goal]
    What is the minimum value of price of in the given csv file? 
    CSV: price.csv
    Column: price
    Skill: CSV_Reader
    [Output]
    {
        "description": "Function that returns the minimum price value in the csv file",
        "name": "get_min_price",
        "function": """
def get_min_price(csv_file_path) -> str:
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file_path)

        # Find the minimum price value
        min_price = df['Price'].min()

        return min_price
    except Exception as e:
        return f'Error: {str(e)}'
    """,
        "library": ["import pandas as pd"],
        "parameters": {
            "csv_file_path": "price.csv"
        },
        "output_type": "float",
        "call": "get_min_price('price.csv')"
    }


    [Goal]
    {{$input}}
    [Output]
    '''

    return sk_prompt