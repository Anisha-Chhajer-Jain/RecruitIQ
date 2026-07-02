import pandas as pd
import json
import os

def load_jd(filepath: str) -> str:
    """Loads the job description text."""
    if filepath.endswith('.docx'):
        from docx import Document
        doc = Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()

def load_candidates(filepath: str) -> pd.DataFrame:
    """Loads the candidates dataset (CSV, JSON, or JSONL)."""
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith('.jsonl'):
        df = pd.read_json(filepath, lines=True)
    elif filepath.endswith('.json'):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV, JSON, or JSONL file.")
    return df

def print_schema_summary(df: pd.DataFrame):
    """Prints a schema summary of the candidates DataFrame."""
    print("=== Candidate Dataset Schema Summary ===")
    print(f"Total Rows: {len(df)}")
    print(f"Total Columns: {len(df.columns)}")
    print("\nColumns and Data Types:")
    print(df.dtypes)
    print("\nNull Counts:")
    print(df.isnull().sum())
    print("\nFirst 3 Rows (Preview):")
    print(df.head(3).to_string())
    print("========================================")

def clean_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: handle missing values, normalize text, dedupe."""
    # Deduplicate rows by candidate_id if it exists
    if 'candidate_id' in df.columns:
        df = df.drop_duplicates(subset=['candidate_id'])
    else:
        # Try to drop completely duplicate rows, but ignore if there are unhashable types
        try:
            df = df.drop_duplicates()
        except TypeError:
            pass
    
    # Text normalization: strip whitespace for string columns
    for col in df.columns:
        if df[col].dtype == 'object':
            # Convert to string and strip whitespace
            # Pandas read_csv might read empty as NaN, handle that first
            df[col] = df[col].fillna('')
            df[col] = df[col].astype(str).str.strip()
            
    # For numerical columns, fill NaNs with 0
    num_cols = df.select_dtypes(include=['number']).columns
    df[num_cols] = df[num_cols].fillna(0)
    
    return df

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test data loading")
    parser.add_argument('--jd', type=str, default='sample_data/job_description.txt')
    parser.add_argument('--candidates', type=str, default='sample_data/candidates.csv')
    args = parser.parse_args()

    jd_path = args.jd
    candidates_path = args.candidates
    
    if os.path.exists(jd_path) and os.path.exists(candidates_path):
        jd_text = load_jd(jd_path)
        print("Successfully loaded Job Description. Length:", len(jd_text))
        print("\n")
        
        df = load_candidates(candidates_path)
        print_schema_summary(df)
        
        # cleaned_df = clean_candidates(df)
        # print(f"\nAfter cleaning: {len(cleaned_df)} rows remaining.")
    else:
        print(f"Data not found at {jd_path} and/or {candidates_path}.")
