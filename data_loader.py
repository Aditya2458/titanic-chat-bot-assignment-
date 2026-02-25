"""
Data loader module for Titanic dataset
"""
import pandas as pd
import os

# Get the path to the dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "titanic.csv")

def load_titanic_data() -> pd.DataFrame:
    """
    Load the Titanic dataset from CSV file.
    
    Returns:
        pd.DataFrame: The Titanic dataset
    """
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        # Try alternative path
        alt_path = os.path.join(os.getcwd(), "data", "titanic.csv")
        df = pd.read_csv(alt_path)
        return df

def get_dataset_info() -> dict:
    """
    Get basic information about the Titanic dataset.
    
    Returns:
        dict: Dataset info including columns, shape, etc.
    """
    df = load_titanic_data()
    
    # Convert numpy types to native Python types for JSON serialization
    return {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
        "missing_values": {k: int(v) for k, v in df.isnull().sum().to_dict().items()}
    }

# Test the data loader
if __name__ == "__main__":
    df = load_titanic_data()
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
