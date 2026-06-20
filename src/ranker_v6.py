import json
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==================================================
# JD
# ==================================================

jd_text = """
Senior AI Engineer

Need:
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

jd_embedding = model.encode(jd_text)

# ==================================================
# TITLE SCORES
# ==================================================

TITLE_SCORES = {

    "Recommendation Systems Engineer":1.0,
    "Search Engineer":1.0,
    "Senior AI Engineer":0.95,
    "Lead AI Engineer":0.95,
    "Applied ML Engineer":0.95,
    "Machine Learning Engineer":0.90,
    "NLP Engineer":0.90,
    "ML Engineer":0.85,
    "AI Engineer":0.85,
    "AI Research Engineer":0.80,
    "Senior Software Engineer (ML)":0.80,
    "Data Scientist":0.70
}

# ==================================================
# COMPANY SCORES
# ==================================================

PRODUCT_COMPANIES = {

    "Google",
    "Apple",
    "Uber",
    "Swiggy",
    "Zomato",
    "Meesho",
    "Flipkart",
    "PhonePe",
    "Razorpay",
    "Yellow.ai",
    "Aganitha"
}

SERVICE_COMPANIES = {

    "TCS",
    "Infosys",
    "Wipro",
    "Capgemini",
    "Cognizant",
    "HCL",
    "Accenture",
    "Tech Mahindra",
    "Mphasis"
}

# ==================================================
# FEATURE TERMS
# ==================================================

RETRIEVAL_TERMS = [

    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "semantic search",
    "embedding",
    "embeddings",
    "vector search",
    "vector database",
    "bm25",
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "learning-to-rank",
    "ltr",
    "hybrid retrieval",
    "information retrieval"
]

PRODUCTION_TERMS = [

    "production",
    "deployed",
    "deployment",
    "serving",
    "inference",
    "latency",
    "api",
    "real-time",
    "monitoring",
    "docker",
    "kubernetes",
    "mlops"
]

EVALUATION_TERMS = [

    "ndcg",
    "mrr",
    "precision",
    "recall",
    "evaluation",
    "a/b",
    "ab test",
    "human judgments",
    "offline metrics",
    "online metrics",
    "relevance labeling"
]

AI_TERMS = [

    "llm",
    "nlp",
    "transformers",
    "rag",
    "embeddings",
    "retrieval",
    "ranking",
    "recommendation",
    "prompt engineering"
]

NEGATIVE_TERMS = [

    "mechanical engineer",
    "civil engineer",
    "graphic designer",
    "hr manager",
    "accountant",
    "sales executive",
    "operations manager",
    "content writer",
    "customer support",
    "marketing",
    "business analyst",
    "project manager",
    "qa engineer",
    "test automation"
]

# ==================================================
# HELPER
# ==================================================

def feature_score(text, terms, weight):

    hits = 0

    for t in terms:

        if t.lower() in text:
            hits += 1

    return min(hits * weight, 1)


# ==================================================
# MAIN
# ==================================================

results=[]

print("Processing candidates...")

with open(
    "data/raw/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for idx,line in enumerate(f):

        c=json.loads(line)

        profile=c["profile"]
        signals=c["redrob_signals"]

        title=profile["current_title"]
        company=profile["current_company"]
        exp=profile["years_of_experience"]

        text=[]

        text.append(profile.get("headline",""))
        text.append(profile.get("summary",""))

        for s in c.get("skills",[]):

            text.append(
                s["name"]
            )

        for h in c.get("career_history",[]):

            text.append(
                h["title"]
            )

            text.append(
                h["description"]
            )

        full_text=" ".join(text)

        lower=full_text.lower()

        # ==========================

        embedding=model.encode(
            full_text
        )

        semantic_score=cosine_similarity(
            [jd_embedding],
            [embedding]
        )[0][0]

        retrieval_score=feature_score(
            lower,
            RETRIEVAL_TERMS,
            .08
        )

        production_score=feature_score(
            lower,
            PRODUCTION_TERMS,
            .08
        )

        evaluation_score=feature_score(
            lower,
            EVALUATION_TERMS,
            .10
        )

        ai_score=feature_score(
            lower,
            AI_TERMS,
            .08
        )

        negative_score=feature_score(
            lower,
            NEGATIVE_TERMS,
            .25
        )

        title_score=TITLE_SCORES.get(
            title,
            .30
        )

        # ==========================

        if 5 <= exp <= 9:

            exp_score=1

        elif 4 <= exp <= 12:

            exp_score=.7

        else:

            exp_score=.3

        github=max(
            signals[
            "github_activity_score"
            ],
            0
        )/100

        behavior_score=(

            signals[
            "recruiter_response_rate"
            ]

            + github +

            signals[
            "interview_completion_rate"
            ]

        )/3

        # ==========================

        if company in PRODUCT_COMPANIES:

            company_score=1

        elif company in SERVICE_COMPANIES:

            company_score=.2

        else:

            company_score=.5

        # ==========================

        final_score=(

            .30*semantic_score+

            .25*retrieval_score+

            .15*title_score+

            .10*production_score+

            .05*evaluation_score+

            .05*ai_score+

            .05*exp_score+

            .03*behavior_score+

            .02*company_score

        )

        final_score -= negative_score

        # ==========================

        results.append({

            "candidate_id":
            c["candidate_id"],

            "title":
            title,

            "company":
            company,

            "semantic_score":
            round(semantic_score,3),

            "retrieval_score":
            round(retrieval_score,3),

            "production_score":
            round(production_score,3),

            "evaluation_score":
            round(evaluation_score,3),

            "ai_score":
            round(ai_score,3),

            "negative_score":
            round(negative_score,3),

            "final_score":
            round(final_score,4)

        })

        if idx>=5000:
            break


# ==================================================
# OUTPUT
# ==================================================

df=pd.DataFrame(results)

df=df.sort_values(
    "final_score",
    ascending=False
)

print("\nTOP 30\n")
print(df.head(30))


df.head(100).to_csv(
    "outputs/top100_v6.csv",
    index=False
)

print(
    "\nSaved outputs/top100_v6.csv"
)