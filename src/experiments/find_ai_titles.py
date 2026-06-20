import json
import pandas as pd

rows = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        candidate = json.loads(line)

        rows.append({
            "title": candidate["profile"]["current_title"]
        })

df = pd.DataFrame(rows)

keywords = [
    "AI",
    "ML",
    "Machine",
    "Data Scientist",
    "NLP",
    "Search",
    "Recommendation",
    "Applied"
]

for keyword in keywords:
    print("\n==========", keyword, "==========")

    matches = df[
        df["title"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    print(matches["title"].value_counts().head(30))