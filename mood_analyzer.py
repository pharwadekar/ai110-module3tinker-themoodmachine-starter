# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.
"""

from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.
        """
        import re
        cleaned = text.strip().lower()
        # Replace basic punctuation with spaces, but keep emojis and slashes for text faces
        cleaned = re.sub(r'[!.,?"\']', ' ', cleaned)
        tokens = cleaned.split()

        return tokens

    def score_text(self, text: str) -> int:
        """
        Compute a numeric "mood score" for the given text.
        """
        tokens = self.preprocess(text)
        score = 0
        skip_next = False
        
        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue
                
            # Handle simple negation ("not happy", "never fun")
            if token in ["not", "never", "no"]:
                if i + 1 < len(tokens):
                    next_token = tokens[i+1]
                    if next_token in self.positive_words:
                        score -= 1  # "not happy" -> negative
                        skip_next = True
                        continue
                    elif next_token in self.negative_words:
                        score += 1  # "not bad" -> positive
                        skip_next = True
                        continue
            
            if token in self.positive_words:
                score += 1
            elif token in self.negative_words:
                score -= 1
                
        return score

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.
        """
        tokens = self.preprocess(text)
        score = self.score_text(text)
        
        pos_count = sum(1 for t in tokens if t in self.positive_words)
        neg_count = sum(1 for t in tokens if t in self.negative_words)
        
        if score > 0:
            if neg_count > 0:  # e.g., positive overall, but has negative words
                return "mixed"
            return "positive"
        elif score < 0:
            if pos_count > 0:
                return "mixed"
            return "negative"
        else:
            if pos_count > 0 and neg_count > 0:
                return "mixed"
            return "neutral"

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = self.score_text(text)

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
            if token in self.negative_words:
                negative_hits.append(token)

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )
