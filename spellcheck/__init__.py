import os

def split_text_into_chunks_on_whitespace(text, chunk_size=50000):
    chunks = []
    # Start index of the current chunk
    start_index = 0
    
    while start_index < len(text):  # Continue until end of text
        # If the remaining text is shorter than the chunk size, add it to the chunks list and break
        if len(text) - start_index <= chunk_size:
            chunks.append(text[start_index:])
            break
        
        # Find the last whitespace character in the text before the chunk size limit
        end_index = text.rfind(' ', start_index, start_index + chunk_size)
        
        # If no whitespace is found, we fallback to cutting the word
        if end_index == -1:
            end_index = start_index + chunk_size
        
        # Add the chunk to the list
        chunks.append(text[start_index:end_index])
        
        # Update the start index to the end of the current chunk
        start_index = end_index + 1  # Skip the whitespace
    
    return chunks

def load_data_into_list(data_folder):
    all_text_list = []
    files = os.listdir(data_folder)
    for file in files:
        if file != "all_possible_words.txt":
            with open(f"{data_folder}/{file}") as f:
                text = f.read()
                chunks = split_text_into_chunks_on_whitespace(text)
                all_text_list.extend(chunks)
    return all_text_list