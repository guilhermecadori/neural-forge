import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle, json, os

train = pd.read_csv('data/processed/train.csv')
test = pd.read_csv('data/processed/test.csv')
X_train = train.drop('Churn', axis=1)
y_train = train['Churn']
X_test = test.drop('Churn', axis=1)
y_test = test['Churn']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

os.makedirs('models', exist_ok=True)

with open('models/model.pkl', 'wb') as f:
    pickle.dump(model, f)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

with open("metrics.json", "w") as f:
    json.dump({"accuracy": acc}, f, indent=2)