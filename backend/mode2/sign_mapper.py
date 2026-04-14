import json
import os
import difflib
import config

class SignMapper:
    def __init__(self):
        self.dictionary = {}
        if os.path.exists(config.SIGN_DICT_PATH):
            try:
                with open(config.SIGN_DICT_PATH, 'r', encoding='utf-8') as f:
                    self.dictionary = json.load(f)
            except Exception as e:
                print(f"Error loading sign dictionary: {e}")
                
    def lookup(self, word):
        word = word.lower()
        if word in self.dictionary:
            return self.dictionary[word], "exact"
            
        matches = difflib.get_close_matches(word, self.dictionary.keys(), n=1, cutoff=0.8)
        if matches:
            match = matches[0]
            return self.dictionary[match], "fuzzy"
            
        return None, "not_found"
        
    def get_all_words(self):
        return sorted(list(self.dictionary.keys()))
