import json

TARGET_IDS = [
    "CAND_0002025",
    "CAND_0000031",
    "CAND_0003791",
    "CAND_0004402"
]

print()

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        candidate_id = c["candidate_id"]

        if candidate_id not in TARGET_IDS:
            continue

        profile = c["profile"]
        signals = c["redrob_signals"]

        print("=" * 80)
        print("Candidate ID:", candidate_id)
        print()

        print("TITLE:")
        print(profile.get("current_title", "N/A"))
        print()

        print("COMPANY:")
        print(profile.get("current_company", "N/A"))
        print()

        print("INDUSTRY:")
        print(profile.get("current_industry", "N/A"))
        print()

        print("EXPERIENCE:")
        print(profile.get("years_of_experience", "N/A"))
        print()

        print("HEADLINE:")
        print(profile.get("headline", ""))
        print()

        print("SUMMARY:")
        print(profile.get("summary", ""))
        print()

        print("TOP SKILLS:")

        skills = c.get("skills", [])

        for skill in skills[:15]:
            print("-", skill.get("name", ""))

        print()

        print("BEHAVIORAL SIGNALS:")
        print()

        print(
            "Recruiter Response Rate:",
            signals.get("recruiter_response_rate")
        )

        print(
            "Github Score:",
            signals.get("github_activity_score")
        )

        print(
            "Interview Completion:",
            signals.get("interview_completion_rate")
        )

        print(
            "Open To Work:",
            signals.get("open_to_work_flag")
        )

        print(
            "Notice Period:",
            signals.get("notice_period_days")
        )

        print()

        print("WHY THIS CANDIDATE IS STRONG:")
        print()

        title = profile.get("current_title", "")

        if "AI" in title:
            print("✓ AI-focused title")

        if "ML" in title:
            print("✓ ML-focused title")

        if "Data Scientist" in title:
            print("✓ Data Science experience")

        github = signals.get(
            "github_activity_score",
            0
        )

        if github > 50:
            print("✓ Strong GitHub activity")

        response = signals.get(
            "recruiter_response_rate",
            0
        )

        if response > 0.7:
            print("✓ Highly responsive candidate")

        interview = signals.get(
            "interview_completion_rate",
            0
        )

        if interview > 0.8:
            print("✓ Strong interview completion")

        if signals.get("open_to_work_flag"):
            print("✓ Open to work")

        notice = signals.get(
            "notice_period_days",
            180
        )

        if notice <= 30:
            print("✓ Quick availability")

        elif notice <= 60:
            print("✓ Reasonable notice period")

        print()