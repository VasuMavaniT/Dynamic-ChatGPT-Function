import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAITextEmbedding
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from semantic_kernel.connectors.memory.chroma import ChromaMemoryStore
import os 
import shutil
import pandas as pd
import numpy as np

sk_prompt = '''
Note: "You have to assume parameters based on description and output. Use context.variables.get('parameter_name') to get the value of the parameter. Use existing functions or create new functions to get the output" 

[Goal]
What are the total number of records in the dataset?
CSV: price.csv
Skill: CSV_Reader
Column: brand
[Output]
{
    description: "Function that returns the total number of records in the csv file",
    name: "count_records_in_csv",
    function: "
        def count_records_in_csv(context: sk.SKContext) -> str:
            try:
                csv_file_path = context.variables.get('csv_file_path')
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(csv_file_path)
                
                # Get the number of rows in the DataFrame, which corresponds to the number of records
                total_records = len(df)
                
                return total_records
            except Exception as e:
                return f"Error: {str(e)}"",
    library: "pandas",
    "parameters": {"csv_file_path": "price.csv"}
    "Output_type": "int"
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
    "function": "
        def get_brands(context: sk.SKContext) -> str:
            try:
                csv_file_path = context.variables.get('csv_file_path')
                # Read the CSV file into a pandas DataFrame
                df = pd.read_csv(csv_file_path)
                
                # Get the different brands in the DataFrame
                brands = df['brand'].unique()
                
                return brands
            except Exception as e:
                return f'Error: {str(e)}'",
    "library": "pandas",
    "parameters": {"csv_file_path": "price.csv"}
    "Output_type": "list"
}

[Goal]
    What is the price of a refrigerator with Brand whirlpool and Model H?
[Output]
{
    "description": "Function that returns the price of a refrigerator with a given brand and model",
    "name": "get_refrigerator_price",
    "function": "
        def get_refrigerator_price(context: sk.SKContext) -> str:
            csv_file_path = context.variables.get('csv_file_path')
            brand = context.variables.get('brand')
            model = context.variables.get('model')

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)

            # Filter rows by Brand and Model
            filtered_rows = df[(df['Brand'] == brand) & (df['Model'] == model)]

            # Get the price from the first row of the filtered result
            price = filtered_rows.iloc[0]['Price']

            return price
    "library": "pandas",
    "parameters": {"csv_file_path": "price.csv", "brand": "whirlpool", "model": "H"}
    "Output_type": "float"
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
    "function": "
        def get_min_price(context: sk.SKContext) -> str:
            csv_file_path = context.variables.get('csv_file_path')

            # Read CSV file into a pandas DataFrame
            df = pd.read_csv(csv_file_path)

            min_price = df['Price'].min()

            return min_price
    "library": "pandas",
    "parameters": {"csv_file_path": "price.csv"}
    "Output_type": "float"
}

[Goal]
{{$goal}}}
[Output]
'''

async def make_kernel():
    '''This function creates an semantic kernel 
    and adds text completion and text embedding generation services to kernel.
    '''
    kernel = sk.Kernel()

    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment = 'gpt-4'
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    kernel.add_text_completion_service("azureopenaicompletion", AzureChatCompletion(deployment, endpoint, api_key))
    # kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("text-embedding-ada-002", endpoint, api_key))

    print("Kernel is ready")

    return kernel


async def make_kernel_with_memory(memory_name, collection_name, csv_name):
    '''This function creates an semantic kernel 
    and adds text completion and text embedding generation services to kernel.
    It also creates a Chroma memory stores with the name memory_name and
    saves the csv file with the name csv_name to the memory store with the name collection_name.
    '''
    kernel = sk.Kernel()

    endpoint = "https://thirdray-openai-demo-instance-us-east.openai.azure.com"
    api_key = "917bf6ea50214df7a19a1bf1572aab3d"
    deployment = 'gpt-4'

    kernel.add_text_completion_service("azureopenaicompletion", AzureChatCompletion(deployment, endpoint, api_key))
    kernel.add_text_embedding_generation_service("ada", AzureTextEmbedding("text-embedding-ada-002", endpoint, api_key))

    print("Kernel is ready")

    kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory=memory_name))
    # print("Made two new services attached to the kernel and made a Chroma memory store that's persistent.")

    ### ONLY DELETE THE DIRECTORY IF YOU WANT TO CLEAR THE MEMORY
    ### OTHERWISE, SET delete_dir = True

    delete_dir = False

    if (delete_dir):
        dir_path = memory_name
        shutil.rmtree(dir_path)
        kernel.register_memory_store(memory_store=ChromaMemoryStore(persist_directory=dir_path))
        print("⚠️ Memory cleared and reset")

    df = pd.read_csv(csv_name)

    df_string = df.to_string(index=False)
    df_list = df_string.split('\n')

    memoryCollectionName = collection_name
    for i in range(len(df_list)):
        await kernel.memory.save_information_async(memoryCollectionName, id=f"df_list-{i}", text=f"{df_list[i]}")

    return kernel
    