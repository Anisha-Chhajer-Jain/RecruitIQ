import argparse
import os
import pandas as pd
from data_loader import load_candidates, clean_candidates
from jd_parser import parse_jd
from candidate_profiler import build_candidate_profiles
from rule_scorer import compute_rule_scores
from embedding_engine import compute_semantic_scores
from hybrid_ranker import rank_candidates
from reasoning_generator import generate_reasoning

def main():
    parser = argparse.ArgumentParser(description="Candidate Fit Ranker (Hackathon Version)")
    parser.add_argument('--candidates', type=str, required=True, help="Path to candidates dataset")
    parser.add_argument('--output', type=str, default='Quantum_Syndicates.csv', help="Path to save final output")
    args = parser.parse_args()

    print("=== Candidate Fit Ranker Pipeline Started ===")
    
    # 1. Parse JD (Hardcoded for Hackathon)
    print("\n[1/7] Parsing JD (Hardcoded heuristics)...")
    parsed_jd = parse_jd("")
    
    # 2. Load Candidates
    print(f"\n[2/7] Loading Candidates from {args.candidates}...")
    df = load_candidates(args.candidates)
    df = clean_candidates(df)
    
    # 3. Build Profiles
    print("\n[3/7] Building Candidate Profiles...")
    df = build_candidate_profiles(df)
    
    # 4. Rule Scoring & Initial Filtering
    print("\n[4/7] Computing Rule Scores for all candidates...")
    df = compute_rule_scores('output/parsed_jd.json', df)
    
    # To meet the <5 min CPU constraint, we only generate embeddings for the top 1000 candidates
    # based on the initial heuristic rule score.
    print(f"\n[5/7] Filtering to top 1000 candidates before embedding...")
    df = df.sort_values(by='rule_score', ascending=False).head(1000).copy()
    
    # 5. Semantic Scoring
    print(f"\n[6/7] Generating Semantic Scores for top 1000 candidates...")
    df = compute_semantic_scores('output/parsed_jd.json', df)
    
    # 6. Hybrid Rank & Formatting
    print("\n[7/7] Computing Final Hybrid Rank & Generating Reasoning...")
    df = rank_candidates(df)
    
    # Take exactly top 100
    top_100_df = df.head(100).copy()
    
    # Generate reasoning deterministically
    top_100_df = generate_reasoning(top_100_df)
    
    # Format required columns
    top_100_df = top_100_df.rename(columns={'final_score': 'score'})
    final_submission = top_100_df[['candidate_id', 'rank', 'score', 'reasoning']]
    
    # Save output
    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)
    final_submission.to_csv(args.output, index=False)
    
    print(f"\n=== Pipeline Complete ===")
    print(f"Ranked output saved to {args.output}")

if __name__ == "__main__":
    main()
