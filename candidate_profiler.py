import pandas as pd
import json

def build_candidate_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe of candidates and builds standard profile objects
    and a summary text for embedding generation.
    """
    profiles = []
    summaries = []
    
    CONSULTING_FIRMS = {'tcs', 'infosys', 'wipro', 'accenture', 'cognizant', 'capgemini'}
    
    for idx, row in df.iterrows():
        def _parse(val):
            if isinstance(val, str):
                try:
                    return json.loads(val.replace("'", '"')) 
                except:
                    return {}
            return val if pd.notna(val) else {}
            
        def _parse_list(val):
            if isinstance(val, str):
                try:
                    return json.loads(val.replace("'", '"'))
                except:
                    return []
            return val if isinstance(val, list) else []

        profile_data = _parse(row.get('profile', {}))
        career_history = _parse_list(row.get('career_history', []))
        skills_data = _parse_list(row.get('skills', []))
        redrob_signals = _parse(row.get('redrob_signals', {}))
        
        # 1. Extracted skills
        skills = [s.get('name') for s in skills_data if isinstance(s, dict) and s.get('name')]
        
        # 2. Total Experience
        years_of_exp = profile_data.get('years_of_experience', 0)
        if not isinstance(years_of_exp, (int, float)):
            years_of_exp = 0
            
        # 3. Domain(s) & Consulting Check
        domains = set()
        companies = set()
        if profile_data.get('current_industry'):
            domains.add(profile_data.get('current_industry'))
        if profile_data.get('current_company'):
            companies.add(str(profile_data.get('current_company')).lower())
            
        for job in career_history:
            if isinstance(job, dict):
                if job.get('industry'):
                    domains.add(job.get('industry'))
                if job.get('company'):
                    companies.add(str(job.get('company')).lower())
                    
        domains = list(domains)
        
        # 4. Activity/Behavioral Signals
        activity_signals = {
            "profile_completeness_score": redrob_signals.get("profile_completeness_score", 0),
            "recruiter_response_rate": redrob_signals.get("recruiter_response_rate", 0.0),
            "notice_period_days": redrob_signals.get("notice_period_days", 90)
        }
        
        # 5. Honeypot & JD Disqualifier Flags
        honeypot_flags = {
            "expert_skills_0_exp": False,
            "title_chaser": False,
            "consulting_only": False
        }
        
        # Check expert skills with 0 experience
        for s in skills_data:
            if isinstance(s, dict):
                if s.get('proficiency') == 'expert' and s.get('duration_months', 0) == 0:
                    honeypot_flags["expert_skills_0_exp"] = True
                    break
                    
        # Check title chaser (> 4 jobs in short duration, simplified to trajectory score > 6 for now)
        trajectory_score = len(career_history)
        if trajectory_score > 6 and years_of_exp < 5:
            honeypot_flags["title_chaser"] = True
            
        # Check consulting only
        if companies and all(any(cf in comp for cf in CONSULTING_FIRMS) for comp in companies):
            honeypot_flags["consulting_only"] = True

        structured_profile = {
            "candidate_id": row.get('candidate_id', ''),
            "years_of_experience": years_of_exp,
            "skills": skills,
            "domains": domains,
            "activity_signals": activity_signals,
            "honeypot_flags": honeypot_flags,
            "current_title": profile_data.get('current_title', '')
        }
        
        # 6. Profile Summary Text
        skills_text = ", ".join(skills)
        summary = (
            f"Candidate with {years_of_exp} years of experience as a {profile_data.get('current_title', 'professional')}. "
            f"Skills: {skills_text}. "
        )
        
        job_descriptions = [str(job.get('description', '')) for job in career_history if isinstance(job, dict) and job.get('description')]
        if job_descriptions:
            summary += " Experience details: " + " ".join(job_descriptions)[:500]
            
        profiles.append(structured_profile)
        summaries.append(summary)
        
    df['structured_profile'] = profiles
    df['profile_summary_text'] = summaries
    
    return df
