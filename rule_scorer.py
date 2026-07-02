import pandas as pd
import json

def compute_rule_scores(parsed_jd_path: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes heuristic rule scores based on strict JD matching, 
    behavioral signals from redrob_signals, and honeypot detection.
    """
    with open(parsed_jd_path, 'r', encoding='utf-8') as f:
        jd_data = json.load(f)
        
    required_skills = [s.lower() for s in jd_data.get('required_skills', [])]
    min_exp = jd_data.get('min_years_of_experience', 5)
    
    rule_scores = []
    
    for idx, row in df.iterrows():
        # Parse the structured profile we built
        if 'structured_profile' in df.columns:
            prof = row['structured_profile']
        else:
            prof = row  # fallback
            
        skills = [s.lower() for s in prof.get('skills', [])]
        years_of_exp = prof.get('years_of_experience', 0)
        
        score = 0.0
        
        # 1. Skill Matching
        if required_skills:
            matched = set(skills).intersection(required_skills)
            score += (len(matched) / len(required_skills)) * 0.4
            
        # 2. Experience Matching (with curve)
        if years_of_exp >= min_exp:
            score += 0.3
        elif years_of_exp > 0:
            score += 0.3 * (years_of_exp / min_exp)
            
        # 3. Behavioral Signals Multiplier
        activity = prof.get('activity_signals', {})
        response_rate = activity.get('recruiter_response_rate', 0.5)  # Default 0.5
        completion = activity.get('profile_completeness_score', 50) / 100.0
        
        # Base modifier from behavior (0.5 to 1.2)
        behavior_modifier = (response_rate * 0.8) + (completion * 0.2) + 0.2
        
        # Apply modifier
        score = score * behavior_modifier
        
        # 4. JD Disqualifiers & Honeypots (Penalties)
        penalty = 0.0
        
        # Honeypot: Impossible experience
        expert_skills_0_exp = prof.get('honeypot_flags', {}).get('expert_skills_0_exp', False)
        if expert_skills_0_exp:
            penalty += 1.0  # Massive penalty
            
        # Title chaser penalty
        if prof.get('honeypot_flags', {}).get('title_chaser', False):
            penalty += 0.2
            
        # Consulting only penalty (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini)
        if prof.get('honeypot_flags', {}).get('consulting_only', False):
            penalty += 0.3
            
        score = max(0.0, score - penalty)
        rule_scores.append(score)
        
    df['rule_score'] = rule_scores
    return df
