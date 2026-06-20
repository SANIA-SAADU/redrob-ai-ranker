import json
import pandas as pd

print("Filtering candidates...")

# Strongly relevant titles
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

# Relevant industries
target_industries = [
    "AI/ML",
    "SaaS",
    "Fintech",
    "E-commerce",
    "Food Delivery",
    "Conversational AI",
    "HealthTech AI",
    "Transportation",
    "AdTech",
    "AI Services"
]

filtered = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        profile = c["profile"]

        title = profile.get("current_title", "")
        industry = profile.get("current_industry", "")
        exp = profile.get("years_of_experience", 0)

        title_match = any(
            keyword.lower() in title.lower()
            for keyword in target_keywords
        )

        industry_match = industry in target_industries

        experience_match = 4 <= exp <= 12

        if title_match or (industry_match and experience_match):

            filtered.append({
                "candidate_id": c["candidate_id"],
                "title": title,
                "industry": industry,
                "experience": exp
            })

df = pd.DataFrame(filtered)

print("\nFiltered Candidates:")
print(len(df))

print("\nTop Titles:")
print(df["title"].value_counts().head(30))

print("\nTop Industries:")
print(df["industry"].value_counts().head(20))

# Save for later
df.to_csv(
    "outputs/filtered_candidates.csv",
    index=False
)

print("\nSaved:")
print("outputs/filtered_candidates.csv")