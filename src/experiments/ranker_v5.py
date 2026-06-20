import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

JD_TEXT = """
Senior AI Engineer.

Need strong experience in:

embeddings
retrieval systems
ranking systems
recommendation systems
search systems
vector databases
NLP
LLMs
production ML
evaluation frameworks
hybrid retrieval
learning-to-rank
A/B testing
"""

jd_embedding = model.encode(JD_TEXT)

# =====================================================
# TITLE BOOSTS
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
# INDUSTRIES
# =====================================================

GOOD_INDUSTRIES = {
    "AI/ML",
    "SaaS",
    "Fintech",
    "Conversational AI",
    "AI Services",
    "HealthTech AI",
    "E-commerce"
}

# =====================================================
# SERVICE COMPANIES
# =====================================================

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
# DOMAIN TERMS
# =====================================================

POSITIVE_TERMS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "embedding",
    "embeddings",
    "vector search",
    "vector database",
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "milvus",
    "learning-to-rank",
    "ltr",
    "hybrid retrieval",
    "rerank",
    "reranking",
    "information retrieval",
    "relevance",
    "ndcg",
    "mrr",
    "map",
    "ab test",
    "a/b test",
    "evaluation",
    "offline evaluation"
]

NEGATIVE_TERMS = [
    "computer vision",
    "image classification",
    "object detection",
    "speech recognition",
    "marketing",
    "customer support"
]

# =====================================================
# HONEYPOT
# =====================================================

AI_SKILLS = [
    "llm",
    "langchain",
    "peft",
    "transformers",
    "fine-tuning",
    "rag",
    "embedding",
    "vector",
    "retrieval",
    "prompt engineering"
]

BAD_TITLES = {
    "HR Manager",
    "Marketing Manager",
    "Operations Manager",
    "Sales Executive",
    "Customer Support",
    "Project Manager",
    "Accountant"
}

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
        industry = profile["current_industry"]
        experience = profile["years_of_experience"]

        # ======================================
        # BUILD TEXT
        # ======================================

        text_parts = []

        text_parts.append(
            profile.get("headline", "")
        )

        text_parts.append(
            profile.get("summary", "")
        )

        for skill in c.get("skills", []):
            text_parts.append(
                skill.get("name", "")
            )

        career_text = ""

        for job in c.get(
            "career_history",
            []
        ):

            career_text += (
                " "
                + job.get(
                    "title",
                    ""
                )
                + " "
                + job.get(
                    "description",
                    ""
                )
            )

        text_parts.append(career_text)

        candidate_text = " ".join(
            text_parts
        ).lower()

        # ======================================
        # SEMANTIC SCORE
        # ======================================

        candidate_embedding = model.encode(
            candidate_text
        )

        semantic_score = cosine_similarity(
            [jd_embedding],
            [candidate_embedding]
        )[0][0]

        # ======================================
        # TITLE SCORE
        # ======================================

        title_score = (
            TITLE_SCORES.get(
                title,
                0
            ) / 100
        )

        # ======================================
        # INDUSTRY SCORE
        # ======================================

        industry_score = (
            1
            if industry in GOOD_INDUSTRIES
            else 0
        )

        # ======================================
        # EXPERIENCE SCORE
        # ======================================

        if 5 <= experience <= 9:
            experience_score = 1

        elif 4 <= experience <= 12:
            experience_score = 0.7

        else:
            experience_score = 0.3

        # ======================================
        # BEHAVIORAL SCORE
        # ======================================

        response_rate = signals.get(
            "recruiter_response_rate",
            0
        )

        github_score = max(
            0,
            signals.get(
                "github_activity_score",
                0
            )
        ) / 100

        interview_score = signals.get(
            "interview_completion_rate",
            0
        )

        behavior_score = (
            response_rate
            + github_score
            + interview_score
        ) / 3

        # ======================================
        # AVAILABILITY
        # ======================================

        open_to_work = (
            1
            if signals.get(
                "open_to_work_flag",
                False
            )
            else 0
        )

        notice = signals.get(
            "notice_period_days",
            150
        )

        if notice <= 30:
            notice_score = 1

        elif notice <= 60:
            notice_score = 0.7

        else:
            notice_score = 0.3

        availability_score = (
            open_to_work
            + notice_score
        ) / 2

        # ======================================
        # DOMAIN SCORE
        # ======================================

        positive_hits = 0

        for term in POSITIVE_TERMS:

            if term in candidate_text:
                positive_hits += 1

        negative_hits = 0

        for term in NEGATIVE_TERMS:

            if term in candidate_text:
                negative_hits += 1

        domain_score = (
            positive_hits * 0.10
        ) - (
            negative_hits * 0.05
        )

        domain_score = max(
            0,
            min(domain_score, 1)
        )

        # ======================================
        # BASE SCORE
        # ======================================

        final_score = (
            0.25 * semantic_score +
            0.20 * title_score +
            0.20 * domain_score +
            0.15 * behavior_score +
            0.10 * experience_score +
            0.05 * industry_score +
            0.05 * availability_score
        )

        # ======================================
        # SERVICE COMPANY PENALTY
        # ======================================

        if company in SERVICE_COMPANIES:
            final_score -= 0.05

        # ======================================
        # HONEYPOT DETECTION
        # ======================================

        honeypot_penalty = 0

        skill_hits = 0

        for skill in c.get("skills", []):

            skill_name = skill.get(
                "name",
                ""
            ).lower()

            for ai_skill in AI_SKILLS:

                if ai_skill in skill_name:
                    skill_hits += 1

        career_hits = 0

        for term in POSITIVE_TERMS:

            if term in career_text.lower():
                career_hits += 1

        # AI skills but no AI work

        if skill_hits >= 5 and career_hits == 0:
            honeypot_penalty += 0.15

        # Non AI titles

        if title in BAD_TITLES:
            honeypot_penalty += 0.20

        # Very poor recruiter response

        if response_rate < 0.10:
            honeypot_penalty += 0.10

        # Long notice

        if notice >= 120:
            honeypot_penalty += 0.05

        final_score -= honeypot_penalty

        final_score = max(
            0,
            final_score
        )

        results.append({
            "candidate_id":
                c["candidate_id"],
            "title":
                title,
            "company":
                company,
            "industry":
                industry,
            "experience":
                experience,
            "semantic_score":
                round(
                    semantic_score,
                    3
                ),
            "domain_score":
                round(
                    domain_score,
                    3
                ),
            "honeypot_penalty":
                round(
                    honeypot_penalty,
                    3
                ),
            "final_score":
                round(
                    final_score,
                    4
                )
        })

        # testing
        if idx >= 5000:
            break

df = pd.DataFrame(results)

df = df.sort_values(
    "final_score",
    ascending=False
)

print("\nTOP 30\n")
print(df.head(30))

df.head(100).to_csv(
    "outputs/top100_v5.csv",
    index=False
)

print(
    "\nSaved outputs/top100_v5.csv"
)