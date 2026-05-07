# Lecture 4 - Machine Learning

Machine learning uses data to build models that generalize from examples.

## Topics
- Supervised Learning
- Classification
- Nearest-Neighbor
- Perceptron
- SVMs
- Regression
- Loss Functions
- Overfitting
- Regularization
- scikit-learn
- Reinforcement Learning
- Q-Learning
- k-means Clustering

## Supervised Learning
Supervised learning trains a function on labeled data.
- **Classification** maps inputs to categories
- **Regression** maps inputs to continuous values

## Nearest-Neighbor and Perceptron
Nearest-neighbor predicts based on the closest training examples.
Perceptron learns a linear separator by updating weights.

```python
w = w + alpha * (y - y_hat) * x
```

## Support Vector Machines
SVMs maximize the margin between classes and can learn robust boundaries.

## Regression and Loss
Regression minimizes loss, such as:
- **L1 loss**: `|y - y_hat|`
- **L2 loss**: `(y - y_hat)**2`

## Overfitting and Regularization
Overfitting occurs when a model learns the training data too closely.
- Regularization penalizes model complexity to improve generalization.

## Reinforcement Learning
Reinforcement learning trains agents from rewards.
- **Q-Learning** updates value estimates using:

```text
Q(s,a) <- Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))
```

## k-means Clustering
k-means groups data points into clusters by repeatedly updating centroids.
