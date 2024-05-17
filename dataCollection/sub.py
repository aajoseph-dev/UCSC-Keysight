import os
import time  # Import the time module for the sleep function
from dataProcessing import DataFetch

folder_path = "/Users/shaun/Desktop/115b/test"

data_fetch_instance = DataFetch()

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
    # File exists and is a PDF
    # Add your code here
        retry_count = 0
        max_retries = 3 
        while retry_count < max_retries:
            try:
                data_fetch_instance.uploadFile(file_path)
                break 
            except Exception as e:
                print(f"Error uploading {filename}: {e}")
                print(f"Retrying in 5 seconds...")
                time.sleep(5)  
                retry_count += 1
        else:
            print(f"Failed to upload {filename} after {max_retries} retries.")
