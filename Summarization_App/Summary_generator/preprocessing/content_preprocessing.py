import re
import string
import pandas as pd
import tiktoken
import openai

class TextPreprocessor:
    @staticmethod
    def preprocess_text(text):
        if isinstance(text, float):
            return ""  # or any other handling for float values
        lines = text.split('\n')
        processed_lines = []
        for line in lines:
            if not line.strip().startswith(("Phone", "Email", "mail", "e-mail")):
                processed_lines.append(line)

        text = '\n'.join(processed_lines)
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(f"[{string.punctuation}]", "", text)
        # stopwords = set(["the", "and", "is", "in", "it", "to", "of", "a", "an"])
        # text = " ".join(word for word in text.split() if word.lower() not in stopwords)
        text = re.sub(r'\[[0-9]+\]', '', text)
        text = re.sub(r'\([^)]+\)', '', text)
        return text