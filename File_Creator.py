import re
import json

async def write_function_and_values(json_string, file_name):
    function_match = re.search(r'"function": """(.*?)"""', json_string, re.DOTALL)

    extracted_function = function_match.group(1)
        
    pattern = r'"function":\s*""".*?"""'

    # Use re.sub to remove the matched pattern and the extra comma after "name"
    output_json = re.sub(pattern, '', json_string, flags=re.DOTALL)  # Replace input_json with json_string
    cleaned_string = output_json.replace(',\n    ,', ',\n')

    description = re.search(r'"description":\s*"([^"]*)"', cleaned_string).group(1)
    name = re.search(r'"name":\s*"([^"]*)"', cleaned_string).group(1)
    library = re.search(r'"library":\s*\[([\s\S]*?)\]', cleaned_string).group(1).strip()
    parameters = re.search(r'"parameters":\s*{([\s\S]*?)}', cleaned_string).group(1)
    output_type = re.search(r'"output_type":\s*"([^"]*)"', cleaned_string).group(1)
    function_call = re.search(r'"call":\s*"([^"]*)"', cleaned_string).group(1)

    # Strip " from beginning and end of the library string
    library = library.strip('"')

    print(f"Description: {description}")
    print(f"Name: {name}")
    print(f"Library: {library}")
    print(f"Parameters: {parameters}")
    print(f"Output Type: {output_type}")
    print(f"Function Call: {function_call}")

    # Generate the Python code
#     python_code = f"""from semantic_kernel.skill_definition import sk_function
# import semantic_kernel as sk
# {library}

# class DynamicFunction:

#     @sk_function(
#         description="{description}",
#         name="{name}"
#     )
#     {extracted_function}
# """

    python_code = f"""
{library}
{extracted_function}
"""

    # Write the Python code to a file
    with open(f"{file_name}.py", "w") as file:
        file.write(python_code)

    return function_call 