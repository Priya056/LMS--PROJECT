# Lecture 6 - Language

Language processing teaches AI to understand text and speech.

## Topics
- NLP tasks
- Syntax & Semantics
- Context-Free Grammar
- n-grams
- Tokenization
- Markov Models
- Bag-of-Words
- Naive Bayes
- word2vec
- Attention
- Transformers

## NLP Tasks
Natural Language Processing includes:
- summarization
- machine translation
- information extraction
- sentiment classification
- named entity recognition

## Syntax and Semantics
- **Syntax** is sentence structure.
- **Semantics** is meaning.

## Context-Free Grammar
Context-free grammar defines valid sentences with production rules.

```python
import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP
    NP -> D N | N
    VP -> V | V NP
    D -> 'the' | 'a'
    N -> 'she' | 'city' | 'car'
    V -> 'saw' | 'walked'
""")
```

## n-grams and Tokenization
- Tokenization splits text into words or sentences.
- n-grams are sequences of tokens used for prediction.

## Markov Models
Markov models predict the next token using a limited history.

## Bag-of-Words and Naive Bayes
Bag-of-words represents text as word counts.
Naive Bayes classifies text by assuming feature independence.

## word2vec
word2vec learns distributed word embeddings that capture similarity.

## Attention and Transformers
Attention scores determine which inputs are most relevant.
Transformers process tokens in parallel and use self-attention.
