import pandas as pd
from itertools import combinations
from rapidfuzz import process

def check_interactions(medicine_list, csv_path, severity_threshold="major"):
    df = pd.read_csv(csv_path)
    df['drug1_normalized'] = df['drug1_normalized'].str.lower()
    df['drug2_normalized'] = df['drug2_normalized'].str.lower()
    df = df[df['severity'].str.lower() >= severity_threshold.lower()]  # Focus on dangerous

    meds = [m.lower() for m in medicine_list]
    pairs = list(combinations(meds, 2))
    warnings = []

    for d1, d2 in pairs:
        # Fuzzy match for robustness
        match1 = process.extractOne(d1, df['drug1_normalized'].unique(), score_cutoff=90)
        match2 = process.extractOne(d2, df['drug2_normalized'].unique(), score_cutoff=90)
        if match1 and match2:
            d1_m = match1[0]
            d2_m = match2[0]
        else:
            d1_m, d2_m = d1, d2

        match = df[
            ((df['drug1_normalized'] == d1_m) & (df['drug2_normalized'] == d2_m)) |
            ((df['drug1_normalized'] == d2_m) & (df['drug2_normalized'] == d1_m))
        ]
        for _, row in match.iterrows():
            warnings.append(
                f"⚠ Dangerous Interaction: {row['drug1_normalized'].title()} + {row['drug2_normalized'].title()} | "
                f"Severity: {row['severity']} | {row['description']}"
            )

    return warnings