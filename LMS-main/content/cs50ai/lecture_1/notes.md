# Lecture 1 - Knowledge

AI can represent facts and draw conclusions from them. This lecture covers how logic and knowledge representation allow machines to reason.

## Topics
- Propositional Logic
- Model Checking
- Knowledge Engineering
- Clue
- Mastermind
- Inference Rules
- Resolution
- CNF
- First Order Logic

## Propositional Logic
A sentence is an assertion about the world. In propositional logic, sentences are built from propositions and connectives:
- **¬** not
- **∧** and
- **∨** or
- **→** implication
- **↔** biconditional

### Example
- If it didn’t rain, Harry visited Hagrid.
- Harry visited Hagrid or Dumbledore, but not both.
- Harry visited Dumbledore.

From these facts we can infer that it rained.

## Model Checking
Model checking enumerates possible truth assignments (models) and verifies whether a knowledge base entails a query.

```python
def check_all(knowledge, query, symbols, model):
    if not symbols:
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    remaining = symbols.copy()
    p = remaining.pop()
    model_true = model.copy(); model_true[p] = True
    model_false = model.copy(); model_false[p] = False
    return (
        check_all(knowledge, query, remaining, model_true)
        and check_all(knowledge, query, remaining, model_false)
    )
```

## Knowledge Engineering
Knowledge engineering is the process of representing real-world information in a form an AI can reason with.

### Clue and Mastermind
- In **Clue**, the AI uses logical constraints from cards and guesses to eliminate possibilities.
- In **Mastermind**, the AI uses feedback about correct and incorrect positions to narrow the search space.

## Inference Rules
Inference rules derive new facts from known facts.
- **Modus Ponens**: from `P → Q` and `P`, infer `Q`.
- **And Elimination**: from `P ∧ Q`, infer `P` or `Q`.
- **Implication Elimination**: `P → Q` is equivalent to `¬P ∨ Q`.
- **De Morgan’s Laws** and **Biconditional Elimination** are essential transformations.

## Resolution and CNF
Resolution works on sentences in **Conjunctive Normal Form (CNF)** and is a standard technique for automated reasoning.

## First Order Logic
First Order Logic extends propositional logic with quantifiers, predicates, and variables, making it more expressive for complex domains.
