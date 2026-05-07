# Lecture 2 - Uncertainty

When AI has partial information, probability helps it make the best possible decision.

## Topics
- Probability
- Conditional Probability
- Bayes' Rule
- Joint Probability
- Bayesian Networks
- Sampling
- Markov Models
- Hidden Markov Models

## Probability Basics
Probability measures how likely an event is to occur.
- 0 means impossible
- 1 means certain
- The probabilities of all possible worlds sum to 1

## Conditional Probability and Bayes' Rule
Conditional probability is written as `P(a | b)`.

```text
P(a | b) = P(a ∧ b) / P(b)
```

Bayes’ rule allows inference in the opposite direction:

```text
P(b | a) = P(a | b) * P(b) / P(a)
```

## Joint and Marginal Probability
Joint probability describes the likelihood of multiple events together.
- `P(a, b)` is the probability that both a and b are true.
- Marginalization sums over hidden possibilities.

## Bayesian Networks
A Bayesian network is a directed graph where each node is a random variable and edges represent conditional dependencies.
- Each node stores `P(X | parents(X))`
- The joint probability is the product of local probabilities

## Sampling and Approximate Inference
Exact inference can be expensive.
- **Sampling** approximates distributions by generating many examples.
- **Approximate inference** is often more scalable.

## Markov Models
A Markov model assumes the future depends only on a limited history.
- Hidden Markov Models model hidden states that generate observable evidence.
