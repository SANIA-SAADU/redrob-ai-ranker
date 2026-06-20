# =====================================================
# HONEYPOT DETECTOR
# =====================================================

NON_TECH_TITLES = {

    "Marketing Manager",
    "Sales Executive",
    "HR Manager",
    "Customer Support",
    "Operations Manager",
    "Accountant",
    "Content Writer",
    "Business Analyst"

}

AI_KEYWORDS = [

    "llm",
    "llms",
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "nlp",
    "machine learning",
    "deep learning",
    "transformer",
    "langchain",
    "rag",
    "vector database",
    "pinecone",
    "faiss",
    "qdrant",
    "weaviate",
    "embedding",
    "embeddings",
    "fine-tuning",
    "lora",
    "qlora"

]

REAL_AI_TERMS = [

    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "learning to rank",
    "learning-to-rank",
    "bm25",
    "embedding",
    "embeddings",
    "vector",
    "faiss",
    "pinecone",
    "qdrant",
    "weaviate",
    "ml",
    "machine learning",
    "nlp"

]


def honeypot_penalty(candidate):

    penalty = 0

    profile = candidate["profile"]

    title = profile.get(
        "current_title",
        ""
    )

    exp = profile.get(
        "years_of_experience",
        0
    )

    # =====================================
    # Build candidate text
    # =====================================

    text_parts = [

        profile.get(
            "headline",
            ""
        ),

        profile.get(
            "summary",
            ""
        )

    ]

    for skill in candidate.get(
        "skills",
        []
    ):
        text_parts.append(
            skill.get(
                "name",
                ""
            )
        )

    full_text = " ".join(
        text_parts
    ).lower()

    career_text = ""

    for job in candidate.get(
        "career_history",
        []
    ):

        career_text += (
            " " +
            job.get(
                "description",
                ""
            )
        )

    career_text = career_text.lower()

    # =====================================
    # Rule 1
    # Non-tech title + AI keywords
    # =====================================

    ai_hits = 0

    for term in AI_KEYWORDS:

        if term in full_text:
            ai_hits += 1

    if (
        title in NON_TECH_TITLES
        and ai_hits >= 5
    ):
        penalty += 0.15

    # =====================================
    # Rule 2
    # AI skills but no AI work history
    # =====================================

    real_ai_hits = 0

    for term in REAL_AI_TERMS:

        if term in career_text:
            real_ai_hits += 1

    if (
        ai_hits >= 5
        and real_ai_hits == 0
    ):
        penalty += 0.20

    # =====================================
    # Rule 3
    # Too many AI skills
    # Too little experience
    # =====================================

    if (
        ai_hits >= 8
        and exp < 2
    ):
        penalty += 0.15

    # =====================================
    # Rule 4
    # HR / Marketing pretending AI
    # =====================================

    suspicious_titles = {

        "HR Manager",
        "Marketing Manager",
        "Sales Executive",
        "Customer Support"

    }

    if (
        title in suspicious_titles
        and ai_hits >= 3
    ):
        penalty += 0.10

    return min(
        penalty,
        0.50
    )