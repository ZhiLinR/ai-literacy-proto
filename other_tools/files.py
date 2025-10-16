import requests
import os
from io import BytesIO

from const import OPENAI_CLIENT

client = OPENAI_CLIENT

# Responses API
# https://platform.openai.com/docs/guides/tools-file-search

def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    print(result.id)
    return result.id


def list_files(directory_path):
    # Get all files in the directory
    files = os.listdir(directory_path)
    
    # Filter only regular files (ignore directories)
    files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    
    return files

# Example usage:
directory_path = 'family_case_data'
file_names = list_files(directory_path)

# Print the list of file names
print(file_names)

vector_store = client.vector_stores.create(
    name=""
)

print(vector_store.id)
# Replace with your own file path or URL
for name in file_names:
    file_id = create_file(client, "family_case_data/"+name)
    result = client.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=file_id
    )
    print(result)

result = client.vector_stores.files.list(
    vector_store_id=vector_store.id
)
print(result)
