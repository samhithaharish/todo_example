import openai
import json
import os

def extract_todolist(input_file, output_json):
    try:
        with open(input_file, 'r') as file:
            # Read the content of the file
            file_content = file.read()

            # Set up your OpenAI API key
            openai.api_key = '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'

            # Customize the prompt for your specific use case
            prompt = f"Create a todo list based on the following:\n{file_content}"

            # Make a request to the OpenAI API
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200
            )

            # Extract the generated content from the OpenAI response
            generated_content = response['choices'][0]['text']

            # Perform further processing or save the generated content as JSON
            result = {'input_file': input_file, 'generated_content': generated_content}
            
            with open(output_json, 'w') as json_file:
                json.dump(result, json_file, indent=2)

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'todo.txt')
output_json = 'output.json'

result = extract_todolist(input_file, output_json)
