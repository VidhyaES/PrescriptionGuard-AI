import random
import pandas as pd

# Change this if your file name is different
INTERACTION_CSV = "data\interactions.csv"   

df = pd.read_csv(INTERACTION_CSV)

# Normalize drug names
df["drug1_normalized"] = df["drug1_normalized"].str.title()
df["drug2_normalized"] = df["drug2_normalized"].str.title()

# Get ALL unique dangerous medicines from the CSV
DANGEROUS_MEDICINES = sorted(
    set(df["drug1_normalized"]).union(set(df["drug2_normalized"])),
    key=len,
    reverse=True
)

FREQUENCIES = [
    "Once daily", "Twice daily", "After food", "Before food"
]

DURATIONS = [
    "5 days", "7 days", "10 days", "14 days"
]

def get_interacting_pair():
    """Return one guaranteed dangerous interacting pair"""
    row = df.sample(1).iloc[0]
    return row["drug1_normalized"], row["drug2_normalized"]

def get_random_medicines(min_medicines=2, max_medicines=4):
    """
    Returns a list of dangerous medicines (at least one interacting pair)
    - min_medicines: minimum number of medicines (default 2 = one pair)
    - max_medicines: maximum number of medicines
    """
    # Start with one guaranteed interacting pair
    d1, d2 = get_interacting_pair()
    meds = [
        {"name": d1, "frequency": random.choice(FREQUENCIES), "duration": random.choice(DURATIONS)},
        {"name": d2, "frequency": random.choice(FREQUENCIES), "duration": random.choice(DURATIONS)}
    ]

    # Add more dangerous medicines if needed
    current_count = len(meds)
    target = random.randint(min_medicines, max_medicines)
    
    while current_count < target:
        # Pick a random dangerous medicine (not already in list to avoid duplicates)
        extra_med = random.choice([m for m in DANGEROUS_MEDICINES if m not in [med["name"] for med in meds]])
        meds.append({
            "name": extra_med,
            "frequency": random.choice(FREQUENCIES),
            "duration": random.choice(DURATIONS)
        })
        current_count += 1

    random.shuffle(meds)   # Random order
    return meds