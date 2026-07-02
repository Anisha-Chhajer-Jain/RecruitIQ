# RecruitIQ
### Quantum Syndicates — Hackathon Submission

An ultra-fast, **fully offline** AI recruitment pipeline that ranks 100,000 candidate profiles against a Job Description in under 5 minutes — with zero network calls, zero LLM API dependency, and built-in honeypot/fraud filtering.

---

## The Problem

Recruiters sifting through hundreds of thousands of candidates can't rely on keyword filters — they miss genuine fits and let fake or low-signal profiles through. This challenge raised the bar further: do it **at scale (100K candidates), under a hard time budget (<5 min), with no network access** — ruling out hosted LLM APIs entirely.

**RecruitIQ** solves this with a fully local pipeline: a heuristic rule engine narrows the field fast, a local embedding model handles semantic understanding, and a deterministic reasoning layer explains every result — all without a single network call.

---

## Key Features

- 🚀 **Fast at scale** — ranks 100,000 candidates in under 5 minutes on standard hardware
- 🔌 **Fully offline** — no LLM API calls; embedding model weights are cached locally in-repo
- 🕵️ **Honeypot detection** — penalizes implausible profiles (e.g., "0 years experience, expert-level skills")
- 📊 **Explainable output** — every ranked candidate ships with a human-readable, stat-cited justification
- 🎯 **Behavioral weighting** — prioritizes engaged, responsive talent over static keyword matches

---

## Architecture

A **three-pass hybrid ranker**, designed to spend compute only where it matters — cheap heuristics eliminate 99% of the pool before the (relatively) expensive embedding pass runs on a manageable shortlist.

```text
                        [100,000 Candidates]
                                │
                                ▼
        ┌───────────────────────────────────────────┐
        │ PASS 1 — Heuristic Engine                  │
        │  • Parses JSONL → structured profiles      │
        │  • Strict skill / experience matching      │
        │  • Behavioral multiplier (response rate)   │
        │  • Honeypot penalty (e.g. 0-yr "expert")   │
        └───────────────────┬─────────────────────────┘
                             │
                   [Top 1,000 Candidates]
                             │
                             ▼
        ┌───────────────────────────────────────────┐
        │ PASS 2 — Semantic Embedding Model          │
        │  • Loads all-MiniLM-L6-v2 (offline, cached)│
        │  • Embeds JD vs. candidate summaries       │
        │  • Computes cosine similarity               │
        └───────────────────┬─────────────────────────┘
                             │
                    [Top 100 Candidates]
                             │
                             ▼
        ┌───────────────────────────────────────────┐
        │ PASS 3 — Reasoning Generator                │
        │  • Deterministic template-based generation  │
        │  • Cites real candidate stats (no LLM call)  │
        └───────────────────┬─────────────────────────┘
                             ▼
                  [Quantum_Syndicates.csv]
```

**Why this design:** running a semantic model over all 100,000 profiles would blow the time budget. Pass 1 is O(n) and cheap — it does the heavy lifting of elimination using hard signals (skills, experience, honeypot detection) before Pass 2 spends embedding compute only on a shortlist worth ranking semantically. Pass 3 stays deterministic rather than LLM-generated, in line with the "no network" constraint.

---

## Honeypot / Fraud Filtering

Pass 1 flags and penalizes profiles with implausible signal combinations rather than blindly trusting listed skills — e.g. a candidate claiming "expert" proficiency with zero years of relevant experience, or engagement metrics inconsistent with activity history. This keeps low-signal or fabricated profiles from crowding out genuine fits in the shortlist that reaches Pass 2.

---

## Tech Stack

| Component | Tool |
|---|---|
| Data processing | `pandas`, `numpy` |
| Semantic embeddings | `sentence-transformers` — local HuggingFace model `all-MiniLM-L6-v2` |
| Similarity computation | `scikit-learn` (cosine similarity) |
| Data format | JSONL input → CSV output |
| Runtime | Python 3.11+, fully offline |

---

## Project Structure

```text
.
├── main.py                # Pipeline entry point
├── requirements.txt
├── model_cache/            # Pre-cached embedding model weights (offline use)
├── candidates.jsonl        # Input candidate dataset
├── Quantum_Syndicates.csv  # Output — final ranked shortlist
└── README.md
```

---

## Setup

1. Ensure Python 3.11+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> **No-network compliance:** `sentence-transformers` model weights are pre-cached inside this repository under `model_cache/`. The pipeline requires **zero network access** at runtime — no API keys, no external calls.

---

## Usage

Run the full pipeline end-to-end with a single command:

```bash
python main.py --candidates ./candidates.jsonl
```

This reads the candidate dataset, runs all three passes, and writes the final ranked shortlist to `Quantum_Syndicates.csv`.

### Sample Output

```csv
candidate_id,rank,score,reasoning
CAND_0068351,1,0.520,Lead AI Engineer with 6.4 yrs experience; matches 3 AI/ML skills. Highly responsive (rate: 0.86).
CAND_0098454,2,0.518,AI Specialist with 6.6 yrs experience; matches 2 AI/ML skills. Highly responsive (rate: 0.87).
CAND_0071974,3,0.510,Senior AI Engineer with 7.8 yrs experience; matches 3 AI/ML skills. Highly responsive (rate: 0.76).
```

---

## Performance

- **Scale:** 100,000 candidates
- **Runtime:** < 5 minutes end-to-end, single machine, no GPU required
- **Network calls:** 0

---

## Limitations & Future Work

- Honeypot detection is currently rule-based; a learned anomaly-detection model could generalize better to novel fraud patterns.
- Reasoning generation is template-based for speed and offline compliance — an on-device small LLM could produce more nuanced justifications without breaking the no-network constraint.
- Heuristic weights in Pass 1 are hand-tuned; a validation set would allow data-driven weight optimization.

---

## Team

**Quantum Syndicates**