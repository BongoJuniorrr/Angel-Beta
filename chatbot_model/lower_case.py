import json

def lowercase_words(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Recursively convert all string values to lowercase
    def lowercase_recursive(item):
        if isinstance(item, dict):
            return {key: lowercase_recursive(value) for key, value in item.items()}
        elif isinstance(item, str):
            return item.lower()
        elif isinstance(item, list):
            return [lowercase_recursive(element) for element in item]
        else:
            return item
    
    modified_data = lowercase_recursive(data)
    
    with open(output_file, 'w') as f:
        json.dump(modified_data, f, indent=4)

input_json_file = 'intents.json'    # Replace with your input JSON file
output_json_file = 'intents_lower.json'  # Replace with your output JSON file

lowercase_words(input_json_file, output_json_file)
