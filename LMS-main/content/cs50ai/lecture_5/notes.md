# Lecture 5 - Neural Networks

Neural networks learn complex functions by composing many simple processing units.

## Topics
- Activation Functions
- Gradient Descent
- Multilayer Networks
- Backpropagation
- Overfitting/Dropout
- TensorFlow
- Computer Vision
- Image Convolution
- CNNs
- Recurrent Neural Networks

## Activation Functions
Activation functions add nonlinearity.
- Step function
- Sigmoid
- ReLU

## Gradient Descent
Gradient descent updates weights to reduce loss.
- Stochastic gradient descent uses one sample at a time
- Mini-batch gradient descent uses small batches

## Multilayer Networks
Hidden layers allow networks to learn non-linear patterns.

## Backpropagation
Backpropagation computes gradients from output back through the network.

## Overfitting and Dropout
Dropout randomly removes units during training to reduce overfitting.

## TensorFlow
TensorFlow simplifies neural network development.

```python
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=20)
```

## Computer Vision
CNNs apply convolutional filters and pooling to images.

## Recurrent Neural Networks
RNNs process sequences by reusing hidden state across time steps.
