import string

class NLPProcessor:
    def __init__(self):
        self.fillers = {"uh", "um", "like", "you", "know"}
        
    def process(self, raw_text):
        text = raw_text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = text.split()
        
        cleaned_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == "you" and tokens[i+1] == "know":
                i += 2
                continue
            if tokens[i] not in self.fillers:
                cleaned_tokens.append(tokens[i])
            i += 1
            
        return cleaned_tokens
