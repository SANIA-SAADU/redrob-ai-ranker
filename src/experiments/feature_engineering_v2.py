# src/feature_engineering_v2.py

RETRIEVAL_KEYWORDS = [
    "retrieval",
    "search",
    "ranking",
    "recommendation",
    "relevance",
    "vector search",
    "embedding",
    "embeddings",
    "bm25",
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "learning to rank",
    "ltr"
]

PRODUCTION_KEYWORDS = [
    "production",
    "deployed",
    "deployment",
    "serving",
    "real-time",
    "latency",
    "monitoring",
    "inference",
    "mlops",
    "kubernetes",
    "api",
    "pipeline"
]

EVALUATION_KEYWORDS = [
    "evaluation",
    "a/b",
    "ab test",
    "a/b test",
    "ndcg",
    "mrr",
    "map",
    "metrics",
    "offline-online",
    "experiment",
    "experimentation"
]

AI_SKILLS = [
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "sentence transformers",
    "transformers",
    "llms",
    "nlp",
    "pytorch",
    "tensorflow",
    "langchain",
    "hugging face",
    "embeddings",
    "recommendation systems",
    "machine learning",
    "deep learning"
]

PRODUCT_COMPANIES = {
    "Swiggy",
    "Meesho",
    "Flipkart",
    "Razorpay",
    "Zomato",
    "Yellow.ai",
    "Sarvam AI",
    "Krutrim",
    "Apple",
    "Uber",
    "PhonePe",
    "CRED",
    "InMobi",
    "Freshworks",
    "Zoho"
}


def keyword_score(text, keywords):
    """
    Returns score between 0 and 1
    """

    text = text.lower()

    matches = 0

    for keyword in keywords:
        if keyword.lower() in text:
            matches += 1

    score = matches / len(keywords)

    return min(score, 1.0)


def get_retrieval_score(text):

    return keyword_score(
        text,
        RETRIEVAL_KEYWORDS
    )


def get_production_ml_score(text):

    return keyword_score(
        text,
        PRODUCTION_KEYWORDS
    )


def get_evaluation_score(text):

    return keyword_score(
        text,
        EVALUATION_KEYWORDS
    )


def get_company_score(company):

    if company in PRODUCT_COMPANIES:
        return 1.0

    return 0.3


def get_skill_score(skills):

    skill_text = " ".join(skills).lower()

    matches = 0

    for skill in AI_SKILLS:
        if skill.lower() in skill_text:
            matches += 1

    score = matches / len(AI_SKILLS)

    return min(score, 1.0)


def get_behavior_score(signals):

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

    open_to_work = 1 if signals.get(
        "open_to_work_flag",
        False
    ) else 0

    profile_score = signals.get(
        "profile_completeness_score",
        0
    ) / 100

    saved_by = min(
        signals.get(
            "saved_by_recruiters_30d",
            0
        ) / 20,
        1
    )

    score = (
        0.20 * response_rate +
        0.20 * github_score +
        0.20 * interview_score +
        0.15 * open_to_work +
        0.15 * profile_score +
        0.10 * saved_by
    )

    return score
