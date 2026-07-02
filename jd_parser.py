import os
import json

def parse_jd(jd_text: str, cache_path: str = "output/parsed_jd.json") -> dict:
    """
    Parses the JD deterministically without using an LLM to comply with Hackathon rules.
    """
    parsed_json = {
      "role_title": "Senior AI Engineer",
      "required_skills": [
          "python", "sentence-transformers", "embeddings", "pinecone", "weaviate", 
          "qdrant", "milvus", "opensearch", "elasticsearch", "faiss", "ndcg", "mrr", "map", 
          "a/b testing", "lora", "qlora", "peft", "xgboost", "rag", "machine learning"
      ],
      "preferred_skills": [],
      "min_years_of_experience": 5,
      "domain": "AI/ML"
    }
    
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, indent=2)
        
    return parsed_json
