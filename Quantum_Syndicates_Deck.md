# Slide 1: Title Slide
**Title:** RecruitIQ: Ultra-Fast Offline Candidate Ranking
**Team:** Quantum Syndicates (Chitt Hirpara, Hanuman Singh, Anisha Chhajer, Prashant Parmar)
**Tagline:** Scoring 100,000 candidates in 36 seconds on CPU. Zero Network. Zero Hallucinations.

---

# Slide 2: The Problem (1-line)
**Problem:** Sifting through 100k complex, noisy JSON candidate profiles in under 5 minutes on a CPU-only environment, without relying on external API calls, to find the 100 most engaged and skilled AI Engineers.

---

# Slide 3: Our Approach (The 2-Pass Hybrid Ranker)
**Why Hybrid?** Pure keyword matching gets fooled by honeypots. Pure LLMs fail the compute constraint. Our hybrid approach solves both.

1. **Pass 1 (Heuristic Engine):** Instantly parses 100k candidates, extracting skills and experience. Applies strict behavioral modifiers (response rate) and aggressively penalizes honeypots (0 experience experts).
2. **Pass 2 (Semantic Embedding):** Takes the top 1,000 candidates and uses an offline HuggingFace model (`all-MiniLM-L6-v2`) to compute cosine similarities against the JD.

---

# Slide 4: Architecture Diagram
*(Insert a visual flowchart here based on this logic:)*
[100,000 Candidates] → **Heuristic Engine** → [Top 1,000] → **Semantic Embedding (all-MiniLM-L6-v2)** → [Top 100] → **Reasoning Generator** → [Final CSV]

---

# Slide 5: Key Technical Decisions
- **Offline Model Caching:** We cached the `sentence-transformers` model weights directly inside our GitHub repository to strictly comply with the "No Network" sandbox rule.
- **Behavioral Multipliers:** A candidate with 0% response rate is useless to a recruiter. Our engine mathematically multiplies base scores by a behavioral modifier.
- **Deterministic Reasoning:** We use dynamic Python logic to extract specific candidate facts into a 1-sentence reasoning string, completely eliminating the risk of LLM hallucinations.

---

# Slide 6: Sample Output & Justifications
*(Screenshot of Quantum_Syndicates.csv)*

**Why this candidate is Rank #1:**
*Reasoning: "Lead Ai Engineer with 6.4 yrs experience; matches 3 AI/ML skills. Highly responsive (rate: 0.86)."*
- **Specific Facts:** Cites exact experience (6.4 yrs) and exact skills matched.
- **JD Connection:** The JD requires a Senior/Lead AI Engineer.
- **No Hallucination:** Every data point was extracted directly from their raw profile.

---

# Slide 7: Tech Stack
- **Core Processing:** `pandas`, `numpy` (for ultra-fast vectorized filtering).
- **Embeddings:** `sentence-transformers` (Local CPU-optimized).
- **Ranking / Math:** `scikit-learn` (Cosine Similarity).
- **Deployment:** Standard Python 3.11 Environment.

---

# Slide 8: What We'd Add With More Time
- **Dynamic Skill Expansion:** Using a local lightweight taxonomy tree to equate terms like "PyTorch" and "TensorFlow" to the broader "Deep Learning" requirement.
- **Trajectory Scoring:** Analyzing career velocity (time between promotions) rather than just raw years of experience.
- **Job Duration Weighting:** Penalizing "job hoppers" who have 10 years of experience but spread across 20 companies.
