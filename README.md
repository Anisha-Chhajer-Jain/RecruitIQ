---
title: RecruitIQ Candidate Ranker
emoji: 📈
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
pinned: false
---
# RecruitIQ (Quantum Syndicates Hackathon Submission)

An ultra-fast, entirely local AI recruitment pipeline that matches candidate profiles to Job Descriptions using a heuristic rule engine and semantic embeddings, strictly adhering to hackathon constraints (No Network LLMs).

## Features
- **Phase 1: Heuristic Engine** (Instantly scores 100k candidates against behavioral signals like response rate and explicitly penalizes honeypots).
- **Phase 2: Semantic Embeddings** (Filters to top 1000 candidates and uses local HuggingFace `sentence-transformers` to compute semantic similarity).
- **Phase 3: Deterministic Reasoning** (Generates 1-sentence explanations based on extracted candidate facts without relying on LLM APIs).

## Setup
1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the end-to-end pipeline with the following command:
```bash
python main.py --candidates path/to/candidates.jsonl
```

### Output Format
The pipeline outputs exactly 100 rows matching the standard submission format:
- `candidate_id`
- `rank` (1 is the best)
- `score` (The final hybrid score)
- `reasoning` (A dynamically generated reasoning string)

