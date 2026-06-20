import json
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# =====================================================
# JOB DESCRIPTION
# =====================================================

jd_text = """
Senior AI Engineer.

Need strong experience in:

embeddings,
retrieval systems,
ranking systems,
recommendation systems,
search systems,
vector databases,
NLP,
LLMs,
production ML,
evaluation frameworks,
hybrid retrieval,
learning-to-rank,
A/B testing.
"""

jd_embedding = model.encode(jd_text)

# =====================================================
# TITLE SCORES
# =====================================================

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

# =====================================================
# COMPANIES
# =====================================================

PRODUCT_COMPANIES = {
    "Swiggy",
    "Zomato",
    "Meesho",
    "Razorpay",
    "Flipkart",
    "Uber",
    "Apple",
    "Yellow.ai",
    "Sarvam AI",
    "Krutrim",
    "Haptik",
    "Wysa",
    "PhonePe",
    "Nykaa",
    "Dream11"
}

SERVICE_COMPANIES = {
    "Infosys",
    "TCS",
    "Wipro",
    "Accenture",
    "Capgemini",
    "Cognizant",
    "HCL",
    "Tech Mahindra",
    "Mphasis"
}

# =====================================================
# RETRIEVAL TERMS
# =====================================================

RETRIEVAL_TERMS = [
    "retrieval",
    "search",
    "ranking",
    "recommendation",
    "relevance",
    "learning to rank",
    "learning-to-rank",
    "bm25",
    "faiss",
    "pinecone",
    "weaviate",
    "qdrant",
    "vector search",
    "embedding",
    "embeddings",
    "information retrieval"
]

# =====================================================
# PRODUCTION ML TERMS
# =====================================================

PRODUCTION_TERMS = [
    "production",
    "deployed",
    "deployment",
    "serving",
    "inference",
    "real-time",
    "mlops",
    "kubernetes",
    "monitoring"
]

# =====================================================
# EVALUATION TERMS
# =====================================================

EVAL_TERMS = [
    "ndcg",
    "map",
    "mrr",
    "a/b test",
    "ab test",
    "evaluation",
    "offline metrics",
    "online evaluation"
]

# =====================================================
# FUNCTIONS
# =====================================================

def get_retrieval_score(text):

    text = text.lower()

    hits = 0

    for term in RETRIEVAL_TERMS:
        if term in text:
            hits += 1

    return min(hits * 0.15, 1)


def get_production_ml_score(text):

    text = text.lower()

    hits = 0

    for term in PRODUCTION_TERMS:
        if term in text:
            hits += 1

    return min(hits * 0.12, 1)


def get_evaluation_score(text):

    text = text.lower()

    hits = 0

    for term in EVAL_TERMS:
        if term in text:
            hits += 1

    return min(hits * 0.20, 1)


def get_company_score(company):

    if company in PRODUCT_COMPANIES:
        return 1

    if company in SERVICE_COMPANIES:
        return 0

    return 0.5


# =====================================================
# MAIN
# =====================================================

results = []

print("Processing candidates...")

with open(
    "data/raw/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for idx, line in enumerate(f):

        c = json.loads(line)

        profile = c["profile"]
        signals = c["redrob_signals"]

        title = profile["current_title"]
        company = profile["current_company"]
        experience = profile["years_of_experience"]

        text_parts = [
            profile.get("headline", ""),
            profile.get("summary", "")
        ]

        for skill in c.get("skills", []):
            text_parts.append(
                skill.get("name", "")
            )

        for job in c.get(
            "career_history",
            []
        ):
            text_parts.append(
                job.get("title", "")
            )

            text_parts.append(
                job.get(
                    "description",
                    ""
                )
            )

        candidate_text = " ".join(
            text_parts
        )

        # ====================================
        # SEMANTIC SCORE
        # ====================================

        candidate_embedding = model.encode(
            candidate_text
        )

        semantic_score = cosine_similarity(
            [jd_embedding],
            [candidate_embedding]
        )[0][0]

        # ====================================
        # TITLE SCORE
        # ====================================

        title_score = (
            TITLE_SCORES.get(title, 0)
            / 100
        )

        # ====================================
        # EXPERIENCE SCORE
        # ====================================

        if 5 <= experience <= 9:
            experience_score = 1

        elif 4 <= experience <= 12:
            experience_score = 0.7

        else:
            experience_score = 0.3

        # ====================================
        # BEHAVIOR SCORE
        # ====================================

        response_rate = signals[
            "recruiter_response_rate"
        ]

        github_score = max(
            0,
            signals[
                "github_activity_score"
            ]
        ) / 100

        interview_score = signals[
            "interview_completion_rate"
        ]

        behavior_score = (
            response_rate +
            github_score +
            interview_score
        ) / 3

        # ====================================
        # AVAILABILITY SCORE
        # ====================================

        open_to_work = (
            1
            if signals[
                "open_to_work_flag"
            ]
            else 0
        )

        notice = signals[
            "notice_period_days"
        ]

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

        # ====================================
        # FEATURE ENGINEERING
        # ====================================

        retrieval_score = (
            get_retrieval_score(
                candidate_text
            )
        )

        production_score = (
            get_production_ml_score(
                candidate_text
            )
        )

        evaluation_score = (
            get_evaluation_score(
                candidate_text
            )
        )

        company_score = (
            get_company_score(
                company
            )
        )

        # ====================================
        # FINAL SCORE
        # ====================================

        final_score = (

            0.30 * semantic_score +

            0.20 * retrieval_score +

            0.15 * production_score +

            0.10 * evaluation_score +

            0.10 * behavior_score +

            0.05 * company_score +

            0.05 * title_score +

            0.05 * availability_score

        )

        results.append({

            "candidate_id":
            c["candidate_id"],

            "title":
            title,

            "company":
            company,

            "experience":
            experience,

            "semantic_score":
            round(
                semantic_score,
                3
            ),

            "retrieval_score":
            retrieval_score,

            "production_score":
            production_score,

            "evaluation_score":
            evaluation_score,

            "company_score":
            company_score,

            "final_score":
            round(
                final_score,
                4
            )
        })

        # Testing only
        if idx >= 5000:
            break

# =====================================================
# RESULTS
# =====================================================

df = pd.DataFrame(results)

df = df.sort_values(
    "final_score",
    ascending=False
)

print("\nTOP 30\n")

print(
    df.head(30)
)

df.head(100).to_csv(
    "outputs/top100_v4.csv",
    index=False
)

print(
    "\nSaved outputs/top100_v4.csv"
)