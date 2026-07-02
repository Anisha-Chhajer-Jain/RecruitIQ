# Candidate Fit Ranker

An AI-powered recruitment pipeline that matches candidate profiles to Job Descriptions (JDs) using a hybrid approach of semantic embeddings, hard-rule scoring, and LLM re-ranking.

## Features
- **Phase 1: Data Loader** (Parses complex nested candidate JSON/CSV and DOCX JD files).
- **Phase 2: JD Structurization** (Uses OpenRouter LLMs to extract structured requirements like skills and experience).
- **Phase 3: Candidate Profiling & Embeddings** (Flattens candidate profiles and uses local HuggingFace `sentence-transformers` to compute semantic similarity against the JD).
- **Phase 4: Rule Scoring & Hybrid Ranking** (Calculates hard scores for skill overlap, experience fit, career trajectory, and platform activity, then weights them with the semantic score).
- **Phase 5: LLM Re-Ranking** (Takes the top candidates and uses an LLM to generate a final assessment and a 1-2 sentence justification for their rank).

## Setup
1. Ensure Python 3.9+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenRouter API key (used for JD parsing and LLM re-ranking):
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   OPENROUTER_MODEL=anthropic/claude-3-haiku
   ```

## Usage
Run the end-to-end pipeline with the following command:
```bash
python main.py --jd path/to/job_description.docx --candidates path/to/sample_candidates.json --top_n 15
```

### Arguments:
- `--jd`: Path to the Job Description file (supports `.txt` or `.docx`).
- `--candidates`: Path to the candidate dataset (supports `.csv`, `.json`, `.jsonl`).
- `--output`: (Optional) Where to save the final ranked output. Defaults to `output/ranked_candidates.csv`.
- `--top_n`: (Optional) How many of the top candidates from the hybrid ranker to pass to the LLM for final re-ranking and justification generation. Defaults to 15.

## Output Format
The pipeline outputs a CSV (`output/ranked_candidates.csv`) matching the standard submission format:
- `candidate_id`
- `rank` (1 is the best)
- `score` (The final hybrid score)
- `reasoning` (A short justification from the LLM or hybrid fallback)
