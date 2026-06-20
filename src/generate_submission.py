import pandas as pd

print("Loading ranked candidates...")

df = pd.read_csv(
    "outputs/top100_v6.csv"
)

submission = []

for rank, row in enumerate(
    df.itertuples(),
    start=1
):

    reasons = []

    # Safe column checks
    if hasattr(row, "semantic_score"):
        if row.semantic_score > 0.50:
            reasons.append(
                "Strong semantic match with JD"
            )

    if hasattr(row, "retrieval_score"):
        if row.retrieval_score > 0.30:
            reasons.append(
                "Strong retrieval/search experience"
            )

    if hasattr(row, "production_score"):
        if row.production_score > 0.30:
            reasons.append(
                "Production ML experience"
            )

    if hasattr(row, "evaluation_score"):
        if row.evaluation_score > 0.20:
            reasons.append(
                "Evaluation framework experience"
            )

    if hasattr(row, "industry"):
        if row.industry in [
            "AI/ML",
            "E-commerce",
            "Internet"
        ]:
            reasons.append(
                "Relevant industry background"
            )

    # fallback
    if len(reasons) == 0:
        reasons.append(
            "Relevant AI/ML profile"
        )

    submission.append({

        "candidate_id":
        row.candidate_id,

        "rank":
        rank,

        "reason":
        ", ".join(reasons)
    })

submission_df = pd.DataFrame(
    submission
)

submission_df.to_csv(
    "outputs/submission.csv",
    index=False
)

print("\nSubmission created")

print(
    "\nSaved outputs/submission.csv"
)

print("\nPreview:\n")

print(
    submission_df.head(10)
)