# utils/flashcard_generator.py
import re

def _sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 15]

def generate_flashcards(text, max_cards=8):
    sents = _sentences(text)
    cards = []
    if not sents:
        return cards

    # Use first meaningful sentences as prompt/answer pairs: short question + short answer
    for i, s in enumerate(sents[:max_cards]):
        # Question: ask "What is ..." if sentence defines something, else short prompt
        if re.search(r'\b(is a|is an|refers to|means|defined as)\b', s, flags=re.I):
            # split at "is" for question
            parts = re.split(r'\b(is a|is an|refers to|means|defined as)\b', s, flags=re.I)
            if len(parts) >= 3:
                front = f"What is {parts[0].strip()}?"
                back = parts[-1].strip()
            else:
                front = f"Explain: {s[:60].strip()}"
                back = s
        else:
            front = f"Recall: {s[:60].strip()}..."
            back = s
        cards.append({"front": front, "back": back})
    return cards
