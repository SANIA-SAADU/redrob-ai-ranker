import json
from collections import Counter

print("Loading candidates...")

companies = Counter()

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        candidate = json.loads(line)

        company = candidate["profile"]["current_company"]

        companies[company] += 1

print("\nTop 50 Companies:\n")

for company, count in companies.most_common(50):
    print(f"{company}: {count}")