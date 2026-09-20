from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textblob import TextBlob
import torch

class SpellCheckerModule:
    def __init__(self):
        # Load grammar correction model
        self.tokenizer = AutoTokenizer.from_pretrained("prithivida/grammar_error_correcter_v1")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("prithivida/grammar_error_correcter_v1")

    def correct_spell(self, text):
        # Use TextBlob to correct spelling word-by-word
        words = text.split()
        corrected_words = [str(TextBlob(word).correct()) for word in words]
        return " ".join(corrected_words)

    def correct_grammar(self, text):
        # Ensure input is a string
        if not isinstance(text, str) or not text.strip():
            return "Invalid input for grammar correction."

        # Encode input with prefix required by the model
        inputs = self.tokenizer.encode("gec: " + text, return_tensors="pt")

        # Generate corrected output
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=128,
                num_beams=5,
                early_stopping=True,
                no_repeat_ngram_size=2
            )

        # Decode and return the corrected sentence
        corrected = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected

if __name__ == "__main__":
    checker = SpellCheckerModule()

    test_text = "He go to school every day and she have a apple."
    print("Original:", test_text)

    corrected_spelling = checker.correct_spell(test_text)
    print("Corrected Spelling:", corrected_spelling)

    corrected_grammar = checker.correct_grammar(corrected_spelling)
    print("Corrected Grammar:", corrected_grammar)
