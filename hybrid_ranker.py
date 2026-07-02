import pandas as pd

# Configurable weights
W_SEMANTIC = 0.4
W_RULE = 0.6

def rank_candidates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes final_score by linearly combining semantic and rule scores.
    """
    if 'semantic_score' not in df.columns:
        df['semantic_score'] = 0.0
        
    df['final_score'] = (
        W_SEMANTIC * df['semantic_score'] +
        W_RULE * df['rule_score']
    )
    
    # Sort descending by final score
    df = df.sort_values(by=['final_score', 'candidate_id'], ascending=[False, True]).reset_index(drop=True)
    df['rank'] = df.index + 1
    
    return df
