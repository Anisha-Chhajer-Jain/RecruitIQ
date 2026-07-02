import os
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = 'all-MiniLM-L6-v2'
_model = None

def get_model():
    global _model
    if _model is None:
        print(f"Loading sentence-transformers model '{MODEL_NAME}'... (this may take a moment on first run)")
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def compute_semantic_scores(jd_json_path: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates embeddings for JD and candidate summaries.
    Computes cosine similarity to yield a 'semantic_score'.
    """
    if not os.path.exists(jd_json_path):
        raise FileNotFoundError(f"Parsed JD JSON not found at {jd_json_path}. Run Phase 2 first.")
        
    with open(jd_json_path, 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        
    # Create a JD summary text
    jd_skills = jd_data.get('required_skills', []) + jd_data.get('preferred_skills', [])
    jd_skills_text = ", ".join(jd_skills)
    jd_summary = (
        f"Looking for a {jd_data.get('role_title')} with {jd_data.get('min_experience_years')} years of experience. "
        f"Domain: {jd_data.get('domain')}. "
        f"Skills required: {jd_skills_text}. "
    )
    
    model = get_model()
    
    print("Generating embedding for JD...")
    jd_embedding = model.encode([jd_summary])
    
    print(f"Generating embeddings for {len(df)} candidates...")
    candidate_summaries = df['profile_summary_text'].tolist()
    candidate_embeddings = model.encode(candidate_summaries)
    
    print("Computing cosine similarities...")
    similarities = cosine_similarity(candidate_embeddings, jd_embedding).flatten()
    
    df['semantic_score'] = similarities
    return df

if __name__ == "__main__":
    from data_loader import load_candidates
    from candidate_profiler import build_candidate_profiles
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--jd_json', type=str, default='output/parsed_jd.json')
    parser.add_argument('--candidates', type=str, default='sample_data/candidates.csv')
    args = parser.parse_args()
    
    print(f"Loading {args.candidates}...")
    df = load_candidates(args.candidates)
    df = build_candidate_profiles(df)
    
    # We slice to first 10 for quick testing if large
    if len(df) > 100:
        print(f"Dataset too large for simple test. Taking first 10 rows.")
        df = df.head(10).copy()
        
    try:
        df = compute_semantic_scores(args.jd_json, df)
        print("\n=== Semantic Scoring Results ===")
        print(df[['candidate_id', 'semantic_score']].sort_values(by='semantic_score', ascending=False))
    except Exception as e:
        print(f"Error computing semantic scores: {e}")
