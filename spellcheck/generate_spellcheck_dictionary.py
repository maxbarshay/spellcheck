import os
import spacy
import pandas as pd

from spellcheck import load_data_into_list
from spellcheck.spellchecker import SpellChecker

nlp = spacy.blank("en")

def generate_spellcheck_dictionary(data_folder, keep_proportion: float = 1) -> dict[str, int]:
    """ Generates the spellcheck dictionary by first reading all the text data in `data_folder` and then counting word occurences. It then removes words that are not in `big_list` and writes the word occurences to a text file. 
        Args:
            keep_proportion (float): Specifies that we want to keep the top `keep_proportion` proportion of words in our dictionary. This removes uncommon words that might show up `big_list`, but we do not
            want to consider words for this application. Defaults to 1.
        Returns:
            dict[str, int]: a dictionary with word, count key value pairs containing the words occurring in both the training data and `big_list`.
    """        
    with open(f"{data_folder}/all_possible_words.txt") as f:
        big_list = f.readlines()
        big_list = set([word.strip() for word in big_list if word.strip() != ""])

    # data_4138 = pd.read_csv("data/form_4138_data.csv")
    all_text_list = load_data_into_list("data")

    keep_chars = ["-", "/"]
    delete_chars = ["'", "="]

    vocab_dict = {}
    for text in all_text_list:
        fixedup_text = SpellChecker.fixup_text(text.lower(), keep_punct=keep_chars, delete_punct=delete_chars)
        alpha_tokens = [token.text for token in nlp.tokenizer(fixedup_text) if token.is_alpha]
        for alpha_token in alpha_tokens:
            if alpha_token not in vocab_dict:
                vocab_dict[alpha_token] = 1
            else:
                vocab_dict[alpha_token] += 1

    vocab_dict = {word: count for word, count in sorted(vocab_dict.items(), key=lambda x: (-x[1], x[0])) if word in big_list}

    if keep_proportion != 1:
        cutoff_index = int(len(vocab_dict) * keep_proportion)
        vocab_dict = {word: count for word, count in vocab_dict[:cutoff_index].items()}
        
    os.makedirs("spellcheck_dictionaries", exist_ok=True)
    spellcheck_dict_fp = "spellcheck_dictionaries/spellcheck_dictionary.txt"
    with open(spellcheck_dict_fp, "w") as f:
        for word, count in vocab_dict.items():
            f.write(f"{word} {count}\n")

    print(f"Wrote a dictionary of length {len(vocab_dict)} to {spellcheck_dict_fp}")

    return vocab_dict




if __name__ == "__main__":
    generate_spellcheck_dictionary("data")