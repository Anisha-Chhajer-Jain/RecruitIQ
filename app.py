import gradio as gr
import pandas as pd
import os

from data_loader import load_candidates, clean_candidates
from jd_parser import parse_jd
from candidate_profiler import build_candidate_profiles
from rule_scorer import compute_rule_scores
from embedding_engine import compute_semantic_scores
from hybrid_ranker import rank_candidates
from reasoning_generator import generate_reasoning

def rank(file_obj):
    if file_obj is None:
        return None, None
    
    # 1. Parse JD (hardcoded for Hackathon)
    parse_jd("")
    
    # 2. Load Candidates
    df = load_candidates(file_obj.name)
    df = clean_candidates(df)
    
    # 3. Build Profiles
    df = build_candidate_profiles(df)
    
    # 4. Rule Scoring
    df = compute_rule_scores('output/parsed_jd.json', df)
    
    # Filter to top 1000 (if larger)
    if len(df) > 1000:
        df = df.sort_values(by='rule_score', ascending=False).head(1000).copy()
        
    # 5. Semantic Scoring
    df = compute_semantic_scores('output/parsed_jd.json', df)
    
    # 6. Hybrid Rank
    df = rank_candidates(df)
    
    # Take top 100
    top_100_df = df.head(100).copy()
    top_100_df = generate_reasoning(top_100_df)
    
    top_100_df = top_100_df.rename(columns={'final_score': 'score'})
    final_submission = top_100_df[['candidate_id', 'rank', 'score', 'reasoning']]
    
    out_path = "Quantum_Syndicates.csv"
    final_submission.to_csv(out_path, index=False)
    
    return final_submission, out_path

with gr.Blocks() as demo:
    gr.Markdown("# RecruitIQ Candidate Ranker Sandbox")
    gr.Markdown("Upload a `candidates.jsonl` or `.csv` file to generate the top 100 ranking. This demonstrates the offline pipeline complying with the hackathon rules.")
    
    with gr.Row():
        file_in = gr.File(label="Upload Candidates Dataset")
        btn = gr.Button("Rank Candidates", variant="primary")
        
    with gr.Row():
        df_out = gr.Dataframe(label="Top Candidates")
        
    with gr.Row():
        file_out = gr.File(label="Download Ranked CSV")
        
    btn.click(fn=rank, inputs=file_in, outputs=[df_out, file_out])

if __name__ == "__main__":
    demo.launch()
