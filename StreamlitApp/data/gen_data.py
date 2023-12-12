import pandas as pd
import random

# Creating synthetic data for two patients with specified attributes
data = {
    'gender': ['Male', 'Female'],
    'age': [52, 30],
    'hypertension': [True, False],
    'heart_disease': [True, False],
    'smoking_history': ['Frequent', 'Never'],
    'bmi': [30.5, 22.0],
    'HbA1c_level': [7.2, 5.4],  # Elevated for the first patient, normal for the second
    'blood_glucose_level': [180, 90],  # Elevated for the first patient, normal for the second
    'diabetes': [True, False],
    'activity_minutes': [20, 150],  # Low activity for the first patient, high for the second
    'medication': ['Metformin', 'None'],  # Diabetes medication for the first, none for the second
    'risk_score': [0.9, 0.2]  # Higher risk for the first patient, lower for the second
}

# Converting the data into a pandas DataFrame
df = pd.DataFrame(data)
print(df.head(5))
df.iloc[[0]].to_csv("patient1.csv",index=False)
df.iloc[[1]].to_csv("patient2.csv",index=False)
