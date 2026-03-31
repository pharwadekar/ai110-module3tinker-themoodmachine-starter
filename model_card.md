# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

## 1. Model Overview

**Model type:**  
I explored and compared both the rule-based model and the ML model.

**Intended purpose:**  
To classify short, conversational text snippets (like social media posts) into one of four moods: positive, negative, neutral, or mixed.

**How it works (brief):**  
- **Rule-based version:** Calculates numeric mood scores by mapping tokens to pre-defined lists of positive and negative words. It features elementary negation logic (e.g., flipping "not" values) and considers a text 'mixed' if its words have conflicting polarities.
- **ML version:** Utilizes a "bag of words" feature extraction model (CountVectorizer) passed into a Logistic Regression classifier trained across provided labels.

## 2. Data

**Dataset description:**  
The dataset contains 14 short statements. It began as 6 basic examples and I expanded it to include 8 fresh samples emphasizing slang ("highkey", "tbh"), emojis ("💀", "🥲"), and sarcasm.

**Labeling process:**  
Labels were selected based on human interpretation of the sentence's underlying intention. Some posts were difficult to define—like "Lowkey stressed but kind of proud of myself"—which was labeled 'mixed' due to conflicting internal sentiments. Sarcasm was given the label characterizing its real emotion, not its literal wording. 

**Important characteristics of your dataset:**  
- Included modern internet slang ("no cap", "tbh").
- Intermixed common text emojis as indicators.
- Contained examples testing subtle sarcasm ("I absolutely love getting stuck in traffic" -> true label is negative).
- Has distinct 'mixed' mood variants.

**Possible issues with the dataset:**  
The dataset is significantly too small. It doesn't contain a balanced representation of all ways people can relay diverse sentiments, which easily leads to narrow or biased performance.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Positive words add 1, negative words remove 1. A basic heuristic processes single-word negation (e.g., if "not" is followed by a positive word, the rule decreases the score instead). I additionally mapped the logic so if a sentence had 0 net score but still triggered both lists, it evaluated as "mixed" rather than "neutral".

**Strengths of this approach:**  
It processes simple, polarized sentences perfectly ("I love this class so much" mapped predictably to positive). It is fully transparent. 

**Weaknesses of this approach:**  
It completely failed at sarcasm. "I absolutely love getting stuck in traffic" scored as "mixed" rather than purely negative because the algorithm blindly read "love" as positive and "stuck" as negative, irrespective of irony.

## 4. How the ML Model Works (if used)

**Features used:**  
Bag of words features using CountVectorizer.

**Training data:**  
The exact same 14 instances from `SAMPLE_POSTS` and `TRUE_LABELS` in `dataset.py`.

**Training behavior:**  
Because the model was remarkably tiny with zero test-withheld sets, the logistic regression algorithm flawlessly memorized the training data strings resulting in 100% training accuracy.

**Strengths and weaknesses:**  
- **Strength**: Easily factors together multiple features to interpret labels without manual coding lists or explicit condition writing.
- **Weakness**: Incredible overfitting propensity. Since its known vocabulary is confined exclusively to words found in those 14 strings, evaluating unseen phrasings in an interactive demo is unstable and prone to randomized guesses.

## 5. Evaluation

**How you evaluated the model:**  
We evaluated training accuracy concurrently on the 14 available dataset items.
- Rule-based evaluation achieved roughly 0.64 (64%) accuracy.
- ML models got essentially 1.00 (100%) accuracy, merely reflecting an overfitted training.

**Examples of correct predictions:**  
- `"Just passed the exam!!! 😂"` correctly scored as positive (Rule-based: parsed the joyous emoji; ML: learned the phrase).
- `"Today was a terrible day"` correctly scored as negative on both models due to explicit alignment.

**Examples of incorrect predictions:**  
- Rule-based incorrectly classed `"Lost my wallet today, just perfect. 🥲"` as mixed. The system noticed "perfect" (a positive word) and "lost" (negative), canceling out to a faulty mood, whereas the ML classifier had perfectly tied it to negative.

## 6. Limitations

- The miniature size of the dataset means neither model has generalized understanding.
- The rule-based implementation cannot reliably interpret subtle sentiments such as contextual irony or complicated negations that stretch over multiple gaps.
- There is no separate evaluation or testing partition for the ML set, rendering its true competence invisible.

## 7. Ethical Considerations

- Relying on rigid keyword lists creates blindspots across diverse dialects, regional slangs, or non-native phrasing which may lead to systemic classification disadvantages for those groups.
- Misinterpreting highly critical or distressful messages as 'neutral' or 'mixed' (e.g., a person asking for help ironically) can be dangerous if the analyzer is routing tickets for mental health or emergency resources.

## 8. Ideas for Improvement

- Drastically improve labeled training corpora to hundreds or thousands of instances across diverse speakers.
- Partition out a test split for evaluating Machine Learning generalizations.
- Expand rule-based NLP techniques to analyze broader grammatical syntax structures beyond individual tokens.
- Upgrade to semantic embeddings or a local Transformer-based implementation which better retains inherent context.