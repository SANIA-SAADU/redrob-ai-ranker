import json

print("Building candidate text...")

count = 0

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        text_parts = []

        # headline
        text_parts.append(
            c["profile"].get("headline", "")
        )

        # summary
        text_parts.append(
            c["profile"].get("summary", "")
        )

        # skills
        for skill in c.get("skills", []):
            text_parts.append(
                skill.get("name", "")
            )

        # career history
        for job in c.get("career_history", []):

            text_parts.append(
                job.get("title", "")
            )

            text_parts.append(
                job.get("description", "")
            )

        candidate_text = " ".join(text_parts)

        count += 1

        if count <= 3:
            print("\n-------------------")
            print(c["candidate_id"])
            print(candidate_text[:1000])

print("\nDone")