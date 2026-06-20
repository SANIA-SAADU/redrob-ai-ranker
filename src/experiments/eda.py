import json
import pandas as pd

print("Loading candidates...")

rows = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        rows.append({
            "candidate_id": candidate["candidate_id"],
            "title": candidate["profile"]["current_title"],
            "company": candidate["profile"]["current_company"],
            "industry": candidate["profile"]["current_industry"],
            "experience": candidate["profile"]["years_of_experience"]
        })

print("Creating DataFrame...")

df = pd.DataFrame(rows)

print("\nTotal Candidates:")
print(len(df))

print("\nTop 20 Titles:")
print(df["title"].value_counts().head(20))

print("\nExperience Summary:")
print(df["experience"].describe())

print("\nTop Industries:")
print(df["industry"].value_counts().head(20))