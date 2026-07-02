# RecruitIQ (Quantum Syndicates Hackathon Submission)

**Problem Summary:** Sorting through 100,000 candidate profiles in under 5 minutes without network API calls to find the top 100 fits for a given Job Description, while filtering out honeypots and prioritizing highly engaged talent.

An ultra-fast, entirely local AI recruitment pipeline that matches candidate profiles to Job Descriptions using a heuristic rule engine and semantic embeddings, strictly adhering to all hackathon constraints (No Network LLMs).

## Architecture

Our approach is a high-performance **Two-Pass Hybrid Ranker**:

```text
[100,000 Candidates] 
        │
        ▼
 ┌───────────────────────────────────────┐
 │ Pass 1: Heuristic Engine              │
 │ - Parses JSONL to structured profiles │
 │ - Strict Skill/Experience Matching    │
 │ - Behavioral Multiplier (Response Rate)│
 │ - Honeypot Penalty (e.g., 0 exp expert)│
 └─────────────────┬─────────────────────┘
                   │
           [Top 1,000 Candidates]
                   │
        ▼
 ┌───────────────────────────────────────┐
 │ Pass 2: Semantic Embedding Model      │
 │ - Loads 'all-MiniLM-L6-v2' (offline)  │
 │ - Embeds JD vs Candidate Summaries    │
 │ - Computes Cosine Similarity          │
 └─────────────────┬─────────────────────┘
                   │
           [Top 100 Candidates]
                   │
        ▼
 ┌───────────────────────────────────────┐
 │ Pass 3: Reasoning Generator           │
 │ - Deterministic string generation     │
 │ - Cites actual candidate stats        │
 └─────────────────┬─────────────────────┘
                   ▼
        [Quantum_Syndicates.csv]
```

## Tech Stack
- **Data Processing:** `pandas`, `numpy`
- **Embeddings:** `sentence-transformers` (Local HuggingFace model `all-MiniLM-L6-v2`)
- **Scikit-Learn:** Fast Cosine Similarity computation

## Setup
1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
*(Note: To ensure compliance with the "No Network" sandbox rule, the `sentence-transformers` model weights are cached directly inside this repository in the `model_cache` folder. The pipeline requires zero network access.)*

## Usage
Run the end-to-end pipeline with the single reproduction command:
```bash
python main.py --candidates ./candidates.jsonl
```

### Sample Output (Quantum_Syndicates.csv)
```csv
candidate_id,rank,score,reasoning
CAND_0068351,1,0.520,Lead Ai Engineer with 6.4 yrs experience; matches 3 AI/ML skills. Highly responsive (rate: 0.86).
CAND_0098454,2,0.518,Ai Specialist with 6.6 yrs experience; matches 2 AI/ML skills. Highly responsive (rate: 0.87).
CAND_0071974,3,0.510,Senior Ai Engineer with 7.8 yrs experience; matches 3 AI/ML skills. Highly responsive (rate: 0.76).
```
