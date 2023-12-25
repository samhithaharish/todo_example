import os

def extract_todolist(input_file, output_json):
    try:
        with open(input_file, 'r') as file:
            # Your file processing code here
            pass
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' does not exist.")

# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'todo.txt')
output_json = 'output.json'

result = extract_todolist(input_file, output_json)
