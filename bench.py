import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

y_test = [1,1,0,1,0,0,0,1,1]
y_pred = [0,1,0,1,1,0,1,1,1]

# Calculate metrics
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
accuracy = accuracy_score(y_test, y_pred)

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Accuracy:", accuracy)