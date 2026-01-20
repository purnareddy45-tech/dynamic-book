# utils/notes_generator.py
import re

def _clean_text(text: str) -> str:
    # remove repeated whitespace and weird line breaks
    t = re.sub(r'\r\n', '\n', text)
    t = re.sub(r'\n\s+\n', '\n\n', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

def _first_n_sentences(text: str, n=6):
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return sents[:n]

def generate_notes(text: str) -> str:
    """
    Return a multi-section string with clean, academic notes.
    Sections: Topic Overview, Key Concepts, Definitions, Steps/Procedure (if present),
    Examples (if present), Applications, Key Takeaways.
    """
    text = _clean_text(text)
    if not text:
        return "No content for notes."

    # Topic: first heading-like line or first sentence
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    topic = lines[0] if lines else ""
    if len(topic) > 200:
        # topic should be short; fallback to first sentence
        topic = _first_n_sentences(text, 1)[0] if text else "Topic"

    # Key concepts - extract short phrases from headings / first lines
    key_sentences = _first_n_sentences(text, n=8)

    # Definitions - choose lines with "is a" / "is an" or "means"
    defs = []
    for s in re.split(r'(?<=[.!?])\s+', text):
        if re.search(r'\b(is a|is an|refers to|means|defined as)\b', s, flags=re.I):
            defs.append(s.strip())
            if len(defs) >= 6:
                break

    # Steps / Procedures - look for numbered lists or "Step"/"Procedure"
    steps = []
    for ln in lines:
        if re.match(r'^\d+\.', ln) or re.match(r'^(step|procedure)', ln, flags=re.I):
            steps.append(ln)
            if len(steps) >= 8:
                break

    # Applications / Use cases - take sentences containing "use" or "apply"
    apps = []
    for s in re.split(r'(?<=[.!?])\s+', text):
        if re.search(r'\b(use|apply|application|used in)\b', s, flags=re.I):
            apps.append(s.strip())
            if len(apps) >= 6:
                break

    # Compose notes
    out = []
    out.append(f"Topic Overview:\n{topic}\n")
    out.append("Key Concepts:")
    for i, ks in enumerate(key_sentences, 1):
        out.append(f"{i}. {ks}")
    out.append("")

    if defs:
        out.append("Important Definitions:")
        for d in defs:
            out.append(f"- {d}")
        out.append("")

    if steps:
        out.append("Procedures / Steps:")
        for s in steps:
            out.append(f"- {s}")
        out.append("")

    if apps:
        out.append("Applications / Use Cases:")
        for a in apps:
            out.append(f"- {a}")
        out.append("")

    out.append("Key Takeaways:")
    # heuristically pick last 2-3 sentences as takeaways
    sents = re.split(r'(?<=[.!?])\s+', text)
    last = sents[-3:] if len(sents) >= 3 else sents
    for idx, t in enumerate(last, 1):
        out.append(f"{idx}. {t.strip()}")

    return "\n".join(out)
