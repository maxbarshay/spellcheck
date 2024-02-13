import os
import spacy
from spacy.tokens import Token
import argparse
from symspellpy import SymSpell, Verbosity
import re

class SpellChecker:
    def __init__(self, max_ed=2):
        self.nlp = spacy.blank("en")
        self.spellcheck_dict_fp = "spellcheck_dictionaries/spellcheck_dictionary.txt"
        self.max_ed = max_ed
        self.prefix_length = 3
        self.speller = self.set_up_spellchecker()

    def set_up_spellchecker(self):
        """
        This method initializes the spellchecker with the pre-created dictionary.
        """
        if not os.path.isfile(self.spellcheck_dict_fp):
            raise Exception("You must first generate the spellcheck dictionary by running `python spellcheck/generate_spellcheck_dictionary.py`")

        speller = SymSpell(max_dictionary_edit_distance=self.max_ed, prefix_length=self.prefix_length)
        speller.load_dictionary(self.spellcheck_dict_fp, 0, 1)

        return speller
    
    @staticmethod
    def fixup_text(text:str, keep_punct:list=[], remove_punct:list=[], delete_punct:list=[]) -> str:
        """Perform text preprocessing needed for spellcheck
        Args:
            text (str): text to preprocess
            keep_punct (list, optional): Punctuation to keep. Defaults to [].
            remove_punct (list, optional): Punctuation to remove and replace with a space. Defaults to [].
            delete_punct (list, optional): Punctuation to delete. Defaults to [].
        Returns:
            str: preprocessed text
        """        
        text = text.strip()

        exclude_punct = list(set(['-',',','(', ')',"'", '"', '•', '/', ':', ';', '_', '*', '!', '|','\\','[',']','.']).union(remove_punct) - set(keep_punct))

        # Punctuation not part of the features
        keep = list()
        chars = list(text)
        for ch in chars:
            if ch in delete_punct:
                #Don't add a space for that character
                continue
            elif ch in exclude_punct:
                keep.append(' ')
            else:
                keep.append(ch)

        text = ''.join(keep)

        # Strip other punctuation
        words = text.split()
        keep = list()
        for word in words:
            word = word.strip('-')
            # word = word.strip('.')
            keep.append(word)

        text = ' '.join(keep)
        text = re.sub(r' +', ' ', text)

        return text
    
    def lookup_word(self, token:Token) -> str:
        """This method attempts to spellcheck 'token'. If there is a word within the specified edit distance of 'token' it returns the best option. Otherwise, it just returns the word.
        Args:
            token (Token): spacy token (one word within the larger text)
        Returns:
            str: input or corrected text (if applicable)
        """        
        auto_corrected = self.speller.lookup(token.text, Verbosity.TOP, max_edit_distance=self.max_ed)
        if len(auto_corrected) == 1:
            return auto_corrected[0].term
        else:
            return token.text

    def correct_text(self, text:str) -> str:
        """This method takes in 'text' and spell corrects it returning the spell corrected text. 
        Args:
            text (str): text to correct
        Returns:
            str: corrected text
        """        
        corrected_text = ""
        doc = self.nlp.tokenizer(text)
        for token in doc:
            if token.is_alpha and len(token.text) > 3:
                corrected_word = self.lookup_word(token)
                corrected_text += corrected_word
                corrected_text += token.whitespace_
            else:
                corrected_text += token.text_with_ws
        return corrected_text

    def correct_text_test(self, text:str) -> str:
        """This method is the same as 'correct_text', however it also outputs the words that were spell corrected 
        for testing purposes. 
        Args:
            text (str): text to correct
        Returns:
            str: corrected text
        """        
        corrected_text = ""
        corrected_words = []
        doc = self.nlp.tokenizer(text)
        for token in doc:
            if token.is_alpha and len(token.text) > 3:
                corrected_word = self.lookup_word(token)
                if corrected_word != token.text:
                    corrected_words.append((token.text, corrected_word))
                corrected_text += corrected_word
                corrected_text += token.whitespace_
            else:
                corrected_text += token.text_with_ws
        return corrected_text, corrected_words
        
if __name__ == "__main__":
    text = "To iscape his tarrible flailing, I siezzed hold of my polee stikcing in him."
    parser = argparse.ArgumentParser()
    parser.add_argument("-text", default=text)
    args = parser.parse_args()

    spellchecker = SpellChecker()
    print(f"\nRaw Text:\n{args.text}")
    corrected_text, corrected_words = spellchecker.correct_text_test(args.text)
    print(f"\nSpellchecked Text:\n{corrected_text}\n\nCorrected Words:\n{corrected_words}")