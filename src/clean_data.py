import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

def clean_data(input_path, output_path):
    print(f"Cleaning data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Handle nulls
    df['Age'] = df['Age'].fillna(df['Age'].median())
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    df.drop(columns=['Cabin'], inplace=True) # Too many nulls
    
    # Encoding
    le = LabelEncoder()
    df['Sex'] = le.fit_transform(df['Sex'])
    df['Embarked'] = le.fit_transform(df['Embarked'])
    
    # Scaling (basic for now, will keep it simple for V2)
    # Actually, scaling is often better done after feature engineering, 
    # but the requirement says "scaling" for V2.
    # We'll scale Age and Fare.
    df['Age'] = (df['Age'] - df['Age'].mean()) / df['Age'].std()
    df['Fare'] = (df['Fare'] - df['Fare'].mean()) / df['Fare'].std()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    clean_data("data/raw/train.csv", "data/interim/cleaned_train.csv")
