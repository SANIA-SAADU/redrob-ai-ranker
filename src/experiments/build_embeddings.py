from sentence_transformers import SentenceTransformer
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Put the JD text here (shortened version is okay)
job_description = """
Senior AI Engineer.
Embeddings, retrieval, ranking systems, recommendation systems,
LLMs, NLP, vector databases, evaluation metrics,
production ML systems, hybrid search, recruiter matching.
"""

print("Encoding JD...")
jd_embedding = model.encode(job_description)

results = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for i, line in enumerate(f):

        c = json.loads(line)

        text_parts = []

        text_parts.append(c["profile"].get("headline", ""))
        text_parts.append(c["profile"].get("summary", ""))

        for skill in c.get("skills", []):
            text_parts.append(skill.get("name", ""))

        candidate_text = " ".join(text_parts)

        emb = model.encode(candidate_text)

        score = cosine_similarity(
            [jd_embedding],
            [emb]
        )[0][0]

        results.append({
            "candidate_id": c["candidate_id"],
            "title": c["profile"]["current_title"],
            "score": score
        })

        # Test only first 5000 initially
        if i >= 5000:
            break

df = pd.DataFrame(results)

df = df.sort_values(
    "score",
    ascending=False
)

print(df.head(20))