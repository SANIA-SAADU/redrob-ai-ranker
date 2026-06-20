import json

companies = {}

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        company = c["profile"]["current_company"]

        companies[company] = companies.get(company, 0) + 1

top = sorted(
    companies.items(),
    key=lambda x: x[1],
    reverse=True
)

for company, count in top[:50]:
    print(company, count)