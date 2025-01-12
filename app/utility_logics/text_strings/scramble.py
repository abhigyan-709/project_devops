import random

def scrambled_text(text: str) -> str:

    scrambled_text = ''.join(random.sample(text, len(text)))
    return scrambled_text

print(scrambled_text("Hello World!"))