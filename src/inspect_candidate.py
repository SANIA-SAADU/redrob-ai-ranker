import json

TARGET_IDS = [
    "CAND_0003791",
    "CAND_0004402",
    "CAND_0002025",
    "CAND_0000031"
]

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:
        candidate = json.loads(line)

        if candidate["candidate_id"] in TARGET_IDS:

            print("\n" + "="*80)
            print("Candidate ID:", candidate["candidate_id"])

            profile = candidate["profile"]

            print("\nTITLE:")
            print(profile["current_title"])

            print("\nCOMPANY:")
            print(profile["current_company"])

            print("\nINDUSTRY:")
            print(profile["current_industry"])

            print("\nEXPERIENCE:")
            print(profile["years_of_experience"])

            print("\nHEADLINE:")
            print(profile["headline"])

            print("\nSUMMARY:")
            print(profile["summary"])

            print("\nSKILLS:")
            for skill in candidate.get("skills", [])[:20]:
                print("-", skill["name"])

            print("\nCAREER HISTORY:")

            for job in candidate.get("career_history", []):
                print("\nCompany:", job["company"])
                print("Title:", job["title"])
                print("Description:")
                print(job["description"][:500])

            print("\nSIGNALS:")
            signals = candidate["redrob_signals"]

            print("Open To Work:", signals["open_to_work_flag"])
            print("Recruiter Response Rate:", signals["recruiter_response_rate"])
            print("Github Score:", signals["github_activity_score"])
            print("Interview Completion:", signals["interview_completion_rate"])
            print("Notice Period:", signals["notice_period_days"])