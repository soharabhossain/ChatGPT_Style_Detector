import re
from collections import Counter

class ChatGPTStyleDetector:
    def __init__(self, style_words):
        self.style_words = set(w.strip().lower() for w in style_words if w.strip())

    def analyze_text(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = len(words)
        word_counts = Counter(words)
        style_word_counts = {w: word_counts[w] for w in self.style_words if w in word_counts}
        style_word_total = sum(style_word_counts.values())
        style_score = round((style_word_total / total_words) * 100, 2) if total_words else 0.0
        return {
            'total_words': total_words,
            'style_words_found': style_word_counts,
            'num_style_words': style_word_total,
            'style_score_percent': style_score,
        }

    def highlight_style_words(self, text):
        pattern = r'\b(' + '|'.join(re.escape(word) for word in self.style_words) + r')\b'
        highlighted = re.sub(pattern, r'**\1**', text, flags=re.IGNORECASE)
        return highlighted