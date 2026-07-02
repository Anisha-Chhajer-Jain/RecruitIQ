import pandas as pd
import json

def generate_reasoning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a 1-2 sentence deterministic reasoning string for each candidate
    based on their extracted facts (experience, skills, behavioral signals).
    """
    reasonings = []
    
    for idx, row in df.iterrows():
        if 'structured_profile' in df.columns:
            prof = row['structured_profile']
        else:
            prof = row
            
        title = prof.get('current_title', 'Professional')
        if not title:
            title = 'Professional'
        exp = prof.get('years_of_experience', 0)
        skills = prof.get('skills', [])
        activity = prof.get('activity_signals', {})
        response_rate = activity.get('recruiter_response_rate', 0.0)
        
        # Calculate matching skills conceptually
        ai_skills = [s for s in skills if s.lower() in ['python', 'pytorch', 'tensorflow', 'machine learning', 'llm', 'rag', 'pinecone', 'aws', 'gcp', 'nlp']]
        
        reasoning = f"{title.title()} with {exp:.1f} yrs experience; matches {len(ai_skills)} AI/ML skills. "
        
        # Add behavioral context
        if response_rate > 0.7:
            reasoning += f"Highly responsive (rate: {response_rate:.2f})."
        elif response_rate < 0.3:
            reasoning += f"Low engagement (response rate: {response_rate:.2f})."
        else:
            reasoning += f"Moderate engagement (rate: {response_rate:.2f})."
            
        reasonings.append(reasoning.strip())
        
    df['reasoning'] = reasonings
    return df
