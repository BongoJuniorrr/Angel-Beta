import json

def rename_tags(json_data):
    tag_counts = {}
    for intent in json_data["intents"]:
        tag = intent["tags"]
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1

        intent["tags"] = f"{tag}{tag_counts[tag]}"

    return json_data

# Read the JSON file
with open('intents_lower.json', 'r') as json_file:
    data = json.load(json_file)

# Rename similar tags
data = rename_tags(data)

# Write the modified data back to the JSON file
with open('intents_lower.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
