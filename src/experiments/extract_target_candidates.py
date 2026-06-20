import json
import pandas as pd

target_keywords = [
    "AI",
    "ML",
    "Machine Learning",
    "Data Scientist",
    "NLP",
    "Search",
    "Recommendation",
    "Applied"
]

rows = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        title = c["profile"]["current_title"]

        if any(
            keyword.lower() in title.lower()
            for keyword in target_keywords
        ):
            rows.append({
                "candidate_id": c["candidate_id"],
                "title": title,
                "company": c["profile"]["current_company"],
                "industry": c["profile"]["current_industry"],
                "experience": c["profile"]["years_of_experience"]
            })

df = pd.DataFrame(rows)

print("Candidates Found:")
print(len(df))

print("\nTop Titles:")
print(df["title"].value_counts())

print("\nIndustries:")
print(df["industry"].value_counts().head(20))