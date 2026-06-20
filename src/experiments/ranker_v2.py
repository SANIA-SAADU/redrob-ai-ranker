import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

jd_text = """
Senior AI Engineer.
Embeddings, retrieval systems, ranking systems,
recommendation systems, search systems,
vector databases, NLP, LLMs,
production ML, evaluation frameworks.
"""

jd_embedding = model.encode(jd_text)

TITLE_SCORES = {
    "Recommendation Systems Engineer": 100,
    "Search Engineer": 100,
    "Applied ML Engineer": 95,
    "Senior AI Engineer": 95,
    "Lead AI Engineer": 95,
    "Machine Learning Engineer": 90,
    "NLP Engineer": 90,
    "ML Engineer": 85,
    "AI Engineer": 85,
    "AI Research Engineer": 80,
    "Senior Software Engineer (ML)": 80,
    "Data Scientist": 70
}

GOOD_INDUSTRIES = {
    "AI/ML",
    "SaaS",
    "Fintech",
    "Conversational AI",
    "AI Services",
    "HealthTech AI",
    "E-commerce"
}

results = []

print("Processing candidates...")

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for idx, line in enumerate(f):

        c = json.loads(line)

        profile = c["profile"]
        signals = c["redrob_signals"]

        title = profile["current_title"]
        industry = profile["current_industry"]
        exp = profile["years_of_experience"]

        text_parts = [
            profile.get("headline", ""),
            profile.get("summary", "")
        ]

        for skill in c.get("skills", []):
            text_parts.append(skill.get("name", ""))

        text = " ".join(text_parts)

        emb = model.encode(text)

        semantic_score = cosine_similarity(
            [jd_embedding],
            [emb]
        )[0][0]

        # Title Score
        title_score = TITLE_SCORES.get(title, 0) / 100

        # Industry Score
        industry_score = 1 if industry in GOOD_INDUSTRIES else 0

        # Experience Score
        if 5 <= exp <= 9:
            experience_score = 1
        elif 4 <= exp <= 12:
            experience_score = 0.7
        else:
            experience_score = 0.3

        # Behavioral Score
        response = signals["recruiter_response_rate"]
        github = max(0, signals["github_activity_score"]) / 100
        interview = signals["interview_completion_rate"]

        behavior_score = (
            response +
            github +
            interview
        ) / 3

        # Availability
        open_to_work = 1 if signals["open_to_work_flag"] else 0

        notice = signals["notice_period_days"]

        if notice <= 30:
            notice_score = 1
        elif notice <= 60:
            notice_score = 0.7
        else:
            notice_score = 0.3

        availability_score = (
            open_to_work +
            notice_score
        ) / 2

        final_score = (
            0.35 * semantic_score +
            0.20 * title_score +
            0.15 * behavior_score +
            0.15 * experience_score +
            0.10 * industry_score +
            0.05 * availability_score
        )

        results.append({
            "candidate_id": c["candidate_id"],
            "title": title,
            "industry": industry,
            "experience": exp,
            "score": final_score
        })

        # For testing first
        if idx >= 5000:
            break

df = pd.DataFrame(results)

df = df.sort_values(
    "score",
    ascending=False
)

print(df.head(30))

df.head(100).to_csv(
    "outputs/top100_v2.csv",
    index=False
)

print("\nSaved outputs/top100_v2.csv")