import pandas as pd
import os

def feature_engineering(input_path, output_path):
    print(f"Feature engineering from {input_path}...")
    df = pd.read_csv(input_path)
    
    # New features
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = 0
    df.loc[df['FamilySize'] == 1, 'IsAlone'] = 1
    
    # Title extraction
    # Note: V2 dropped Cabin, but we still have Name in cleaned_train.csv if we didn't drop it.
    # Let's check if Name is there. If not, we might need to adjust clean_data.py.
    if 'Name' in df.columns:
        df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
        df['Title'] = df['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        df['Title'] = df['Title'].replace('Mlle', 'Miss')
        df['Title'] = df['Title'].replace('Ms', 'Miss')
        df['Title'] = df['Title'].replace('Mme', 'Mrs')
        
        # Title mapping
        title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
        df['Title'] = df['Title'].map(title_mapping)
        df['Title'] = df['Title'].fillna(0)
    
    # Drop columns that are no longer needed
    cols_to_drop = ['Name', 'Ticket', 'PassengerId']
    df.drop(columns=[col for col in cols_to_drop if col in df.columns], inplace=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Feature engineered data saved to {output_path}")

if __name__ == "__main__":
    feature_engineering("data/interim/cleaned_train.csv", "data/processed/final_train.csv")
