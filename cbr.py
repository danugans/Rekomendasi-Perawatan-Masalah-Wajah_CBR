from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.metrics import jaccard_score

# Tunable weights for similarity components
WEIGHTS = {
    'symptoms': 0.6,
    'skin_type': 0.15,
    'gender': 0.05,
    'age': 0.2
}

def load_cases(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df

def _symptom_similarity(query_symptoms: List[int], case_symptoms: List[int]) -> float:
    q = np.array(query_symptoms)
    c = np.array(case_symptoms)
    if q.sum() == 0 and c.sum() == 0:
        return 0.0
    try:
        return float(jaccard_score(q, c))
    except Exception:
        inter = float(((q==1) & (c==1)).sum())
        union = float(((q==1) | (c==1)).sum())
        return inter/union if union>0 else 0.0

def _age_similarity(q_age: int, case_age: int, max_age_diff: int = 80) -> float:
    diff = abs(q_age - case_age)
    sim = max(0.0, 1 - (diff / max_age_diff))
    return sim

def compute_similarity(query: Dict[str, Any], case: pd.Series, symptom_columns: List[str]) -> float:
    q_sym = [1 if query.get(sym,0) else 0 for sym in symptom_columns]
    c_sym = [1 if case.get(sym,0) else 0 for sym in symptom_columns]
    s_sym = _symptom_similarity(q_sym, c_sym)
    s_skin = 1.0 if str(query.get('skin_type','')).lower() == str(case.get('skin_type','')).lower() else 0.0
    s_gender = 1.0 if str(query.get('gender','')).lower() == str(case.get('gender','')).lower() else 0.0
    s_age = _age_similarity(int(query.get('age',30)), int(case.get('age',30)))
    sim = (WEIGHTS['symptoms'] * s_sym +
           WEIGHTS['skin_type'] * s_skin +
           WEIGHTS['gender'] * s_gender +
           WEIGHTS['age'] * s_age)
    return sim

def find_similar_cases(query: Dict[str, Any], cases_df: pd.DataFrame, k: int = 3) -> List[Dict]:
    symptom_columns = [c for c in cases_df.columns if c not in ['id','age','gender','skin_type','solution']]
    sims = []
    for _, row in cases_df.iterrows():
        sim = compute_similarity(query, row, symptom_columns)
        sims.append((sim, row))
    sims_sorted = sorted(sims, key=lambda x: x[0], reverse=True)
    topk = sims_sorted[:k]
    results = []
    for sim, row in topk:
        results.append({
            'id': int(row['id']) if 'id' in row else None,
            'similarity': float(sim),
            'age': int(row['age']) if 'age' in row else None,
            'gender': row.get('gender'),
            'skin_type': row.get('skin_type'),
            'solution': row.get('solution'),
            'symptoms': row[[col for col in symptom_columns]].to_dict()
        })
    return results

def recommend_solution(query: Dict[str, Any], cases_df: pd.DataFrame, k: int = 3) -> Dict:
    top_cases = find_similar_cases(query, cases_df, k=k)
    if not top_cases:
        return {'recommendation': 'No similar cases found', 'cases': []}
    best = top_cases[0]
    recommendation = best['solution']
    return {'recommendation': recommendation, 'cases': top_cases}

if __name__ == '__main__':
    print("This module exposes load_cases, find_similar_cases, recommend_solution.")
