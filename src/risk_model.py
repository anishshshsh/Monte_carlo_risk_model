import pandas as pd

def load_risks(path):
    """
    Load risk data from a CSV file.
    """
    return pd.read_csv(path)

def compute_scores(df):
    """
    Compute risk scores based on probability and impact.
    """
    df = df.copy()
    df['Probability'] = pd.to_numeric(df['Probability'], errors='coerce').fillna(0).astype(int)  # Convert to integer
    df['Impact'] = pd.to_numeric(df['Impact'], errors='coerce').fillna(0).astype(int)  
    df['Score'] = df['Probability'] * df['Impact']
    def level(s):
        """
        Determine the risk level based on the score.
        """
        if s >= 15:
            return 'Critical'
        elif s >= 9:
            return 'High'
        elif s >= 5:
            return 'Medium'
        else:
            return 'Low'
    df['Level'] = df['Score'].apply(level)
    return df.sort_values('Score', ascending=False).reset_index(drop=True)  # Sort by score