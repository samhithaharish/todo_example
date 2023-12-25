import openai
import json

# Set your OpenAI API key
api_key = "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"

def extract_todolist(input_file, output_json):
    # Read the text from the input file
    with open(input_file, 'r') as file:
        text = file.read()

    # Define a prompt for the OpenAI API to understand and extract relevant information
    prompt = f"Extract the todo list from the following text:\n{text}"

    # Call the OpenAI API to extract the todo list
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )

    # Extract the extracted todo list from the API response
    extracted_todolist = response['choices'][0]['text'].strip()

    # Write the extracted data to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(extracted_todolist, json_file, indent=4)

    return extracted_todolist

# Example usage:
input_file = r'C:\Users\Samhitha Harish\Desktop\Django-TodoApp-master\todoapp\test\todo.txt'
output_json = "todo.json"
result = extract_todolist(input_file, output_json)
print(result)
