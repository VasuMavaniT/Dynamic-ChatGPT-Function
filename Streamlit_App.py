import streamlit as st
import openai
import datetime
import asyncio
import pandas as pd
import numpy as np
from Kernel import make_kernel
import matplotlib.pyplot as plt
import io
import json
from Prompt import prompt_template
from File_Creator import write_function_and_values
import time

def get_plot(plot_string):
    ''' It Converts the hexadecimal string to binary data, then 
    creates a BytesIO stream from the binary data, then
    reads the plot from the stream and shows it.
    '''
    # Convert the hexadecimal string back to binary data
    plot_binary_data = bytes.fromhex(plot_string)

    # Create a BytesIO stream from the binary data
    plot_binary_stream = io.BytesIO(plot_binary_data)
    
    # Read the plot from the stream and show it
    plot = plt.imread(plot_binary_stream)
    plt.imshow(plot)
    plt.axis('off')  # Turn off axis labels and ticks
    return plt

async def write_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())
    uploaded_file.seek(0)  # Reset the file position indicator to the beginning
    return "Success"

async def main():

    # Streamlit App Title
    st.title("CSV Analysis App")

    # File Upload Section
    st.sidebar.header("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    # Check if a file is uploaded
    if uploaded_file:
        out = await write_file(uploaded_file)
        print("File writing successful")
        df = pd.read_csv(uploaded_file.name)

        # Check if the CSV file has headers
        if not df.columns.any():
            st.warning("Please add headers to the CSV file.")
        else:
            df.to_csv(uploaded_file.name, index=False)
            # Independent Variables Selection (Checkbox)
            st.sidebar.header("Select Independent Variables (X)")
            independent_variables = st.sidebar.multiselect("Select one or more independent variables", df.columns)

            # Check if at least one independent variable is selected
            if not independent_variables:
                st.warning("Please select at least one independent variable.")
            else:
                # Display selected independent variables
                st.write(f"Independent Variables (X): {', '.join(independent_variables)}")

                # User Questions and Responses
                st.sidebar.header("Ask Questions")
                user_question = st.sidebar.text_input("Enter your question:")
                
                # Check if the user has entered a question
                if user_question:
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.read())

                    ask = f'''{user_question} \n
                    Columns: {independent_variables} \n
                    CSV file: {uploaded_file.name}
                    '''

                    print(ask) 

                    kernel = await make_kernel() 

                    sk_prompt = prompt_template()
                    
                    generate_function = kernel.create_semantic_function(prompt_template = sk_prompt,
                                                        description="This function generates a function based on the question and the CSV file",
                                                        max_tokens=3000,
                                                        temperature=0.1,
                                                        top_p=0.5) 
                    
                    # Generate the function
                    value = str(await kernel.run_async(generate_function, input_str=ask)) 
                    st.write(value)

                    function_call = await write_function_and_values(value, "CSV_Reader")
                    time.sleep(2)

                    st.write("Function call is: ", function_call)

                    function_name = function_call.split('(')[0]
                    # print(value)
                    # Convert the string to a dictionary

                    # from CSV_Reader_skill import DynamicFunction
                    # Create an instance of the DynamicFunction class
                    # dynamic_function = DynamicFunction()

                    import CSV_Reader

                    # Call the function
                    try:
                        # result = eval(f'dynamic_function.{function_call}')
                        result = eval(f'CSV_Reader.{function_call}')
                        # result = eval(f'{function_call}')

                        print(result)
                    except Exception as e:
                        result = "Exception occured"
                        print(f'Error: {str(e)}')

                    st.markdown(f"**Final Output:**")
                    st.write(result)
                                        
                else:
                    st.warning("Please enter a question to proceed.")
    else:
        st.warning("Please upload a CSV file and select independent variables to proceed.")

if __name__ == "__main__":
    asyncio.run(main())
