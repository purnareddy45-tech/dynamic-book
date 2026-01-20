# utils/question_bank.py
import re
import random

def _sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 25]

def _choose_keyword(sentence):
    # choose a multi-char word to blank out (prefer nouns/long words)
    words = re.findall(r'\w+', sentence)
    words = [w for w in words if len(w) > 4]
    if not words:
        words = re.findall(r'\w+', sentence)
    return random.choice(words) if words else None

def generate_questions(text):
    sents = _sentences(text)
    mcqs = []
    short_q = []
    long_q = []

    for i, s in enumerate(sents[:6]):
        k = _choose_keyword(s)
        if k:
            # create a blank question
            q_text = s.replace(k, "_____")
            # options: correct + 3 distractors (other words from the text)
            all_words = list(set(re.findall(r'\w{4,}', text)))
            distractors = [w for w in all_words if w.lower() != k.lower()]
            random.shuffle(distractors)
            options = [k] + distractors[:3]
            random.shuffle(options)
            mcqs.append({
                "question": q_text,
                "options": options,
                "answer": k
            })
        else:
            mcqs.append({
                "question": s[:120] + " ?",
                "options": ["A", "B", "C", "D"],
                "answer": "A"
            })

    # short questions: ask to explain first few sentences
    for s in sents[:6]:
        short_q.append(f"Explain: {s[:120].strip()}")

    # long questions: expand on central paragraphs
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]
    for p in paragraphs[:3]:
        long_q.append(f"Discuss in detail: {p[:250].strip()}")

    return {
        "mcqs": mcqs,
        "short_questions": short_q,
        "long_questions": long_q
    }
