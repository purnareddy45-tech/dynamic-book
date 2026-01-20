# utils/summarizer.py
from typing import List
import re

# Try to use transformers if available (optional). If not, fallback.
try:
    from transformers import pipeline
    _HF_AVAILABLE = True
except Exception:
    _HF_AVAILABLE = False

def _simple_sentence_tokenize(text: str) -> List[str]:
    # crude sentence splitter that preserves order
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def _score_sentences(text: str, n_words_window=1):
    # Frequency-based sentence scoring (fallback)
    words = re.findall(r'\w+', text.lower())
    freq = {}
    for w in words:
        if len(w) <= 2: 
            continue
        freq[w] = freq.get(w, 0) + 1
    # normalize
    maxf = max(freq.values()) if freq else 1
    for k in freq:
        freq[k] = freq[k] / maxf
    sents = _simple_sentence_tokenize(text)
    scores = []
    for s in sents:
        swords = re.findall(r'\w+', s.lower())
        score = sum(freq.get(w, 0) for w in swords)
        scores.append((score, s))
    return scores

def _fallback_summary(text: str, max_sentences: int = 5) -> str:
    scores = _score_sentences(text)
    # take top-scoring sentences (preserve document order)
    if not scores:
        return ""
    scores_sorted = sorted(scores, key=lambda x: x[0], reverse=True)
    top = {s for _, s in scores_sorted[:max_sentences]}
    sents = _simple_sentence_tokenize(text)
    selected = [s for s in sents if s in top]
    if not selected:
        # last resort: first few sentences
        selected = sents[:max_sentences]
    return " ".join(selected)

# If HF is available, create a safe summarizer pipeline and a wrapper
if _HF_AVAILABLE:
    try:
        _hf_summarizer = pipeline("summarization", model="google/flan-t5-large")
    except Exception:
        _hf_summarizer = None
else:
    _hf_summarizer = None

def generate_summary(text: str, max_sentences: int = 5) -> str:
    """
    Returns a short professional summary string.
    Tries HuggingFace summarizer; if it fails, uses a robust fallback.
    """
    text = (text or "").strip()
    if not text:
        return "No content to summarize."

    # Keep input length reasonable for HF; trim if extremely long
    if len(text) > 4000:
        text_for_model = text[:4000]
    else:
        text_for_model = text

    # Try HF pipeline first (if available & loaded)
    if _hf_summarizer is not None:
        try:
            out = _hf_summarizer(text_for_model, max_length=200, min_length=40, do_sample=False)
            # transformer summarizers usually return [{'summary_text': '...'}]
            if isinstance(out, list) and out and isinstance(out[0], dict):
                if "summary_text" in out[0]:
                    return out[0]["summary_text"].strip()
                if "generated_text" in out[0]:
                    return out[0]["generated_text"].strip()
        except Exception:
            # fall through to fallback
            pass

    # fallback frequency-based summary
    return _fallback_summary(text, max_sentences=max_sentences)
