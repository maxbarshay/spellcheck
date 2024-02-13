import os

def load_data_into_list(data_folder):
    all_text_list = []
    files = os.listdir(data_folder)
    for file in files:
        with open(f"{data_folder}/{file}") as f:
            text = f.read()
            all_text_list.extend(text)
    return all_text_list