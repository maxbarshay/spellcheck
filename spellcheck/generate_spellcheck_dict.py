import os
import spacy
import pickle
import pandas as pd

from spellcheck import load_data_into_list
from spellcheck.spellchecker import SpellChecker

nlp = spacy.blank("en")

def generate_spellcheck_dictionary(data_folder, keep_proportion: float = 1) -> dict[str, int]:
    """ Generates the proportion of the spellcheck dictionary that comes from scraping the training data and intersecting it with the known vocab.
        Args:
            keep_proportion (float): text to preprocess
        Returns:
            dict[str, int]: a dictionary with word, count key value pairs containing the words occurring in both the training data and the known vocab.
    """        
    with open(f"{data_folder}/all_possible_words.txt") as f:
        big_list = f.readlines()
        big_list = set([word for word in big_list if word.strip() != ""])

    # data_4138 = pd.read_csv("data/form_4138_data.csv")
    all_text_list = load_data_into_list("data")

    keep_chars = ["-", "/"]
    delete_chars = ["'", "="]

    vocab_dict = {}
    for i, row in data_4138.iterrows():
        text = row["TEXT"]
        fixedup_text = SpellChecker.fixup_text(text.lower(), keep_punct=keep_chars, delete_punct=delete_chars)
        alpha_tokens = [token.text for token in nlp.tokenizer(fixedup_text) if token.is_alpha]
        for alpha_token in alpha_tokens:
            if alpha_token not in vocab_dict:
                vocab_dict[alpha_token] = 1
            else:
                vocab_dict[alpha_token] += 1

    vocab_dict = {word: count for word, count in sorted(vocab_dict.items(), key=lambda x: (-x[1], x[0])) if word in known_vocab}

    if keep_proportion != 1:
        cutoff_index = int(len(vocab_dict) * keep_proportion)
        vocab_dict = {word: count for word, count in vocab_dict[:cutoff_index].items()}
        
    os.makedirs("model_artifacts", exist_ok=True)
    spellcheck_dict_fp = "model_artifacts/4138_spellcheck_dict.txt"
    with open(spellcheck_dict_fp, "w") as f:
        for word, count in vocab_dict.items():
            f.write(f"{word} {count}\n")

    print(f"Wrote a dictionary of length {len(vocab_dict)} to {spellcheck_dict_fp}")

    return vocab_dict




if __name__ == "__main__":
    generate_spellcheck_dictionary("data")