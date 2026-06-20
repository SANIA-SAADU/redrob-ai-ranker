import json

TARGET_ID = "CAND_0002344"

with open(
    "data/raw/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidate = json.loads(line)

        if candidate["candidate_id"] == TARGET_ID:

            profile = candidate["profile"]

            print("=" * 80)

            print("Candidate ID:")
            print(candidate["candidate_id"])

            print("\nTitle:")
            print(profile.get("current_title"))

            print("\nCompany:")
            print(profile.get("current_company"))

            print("\nIndustry:")
            print(profile.get("current_industry"))

            print("\nExperience:")
            print(profile.get("years_of_experience"))

            print("\nHeadline:")
            print(profile.get("headline", ""))

            print("\nSummary:")
            print(profile.get("summary", ""))

            print("\nSkills:")

            for skill in candidate.get("skills", []):
                print("-", skill.get("name", ""))

            print("\nCareer History:")

            for job in candidate.get(
                "career_history",
                []
            ):

                print("\nCompany:",
                      job.get("company", ""))

                print("Title:",
                      job.get("title", ""))

                print("Description:")
                print(
                    job.get(
                        "description",
                        ""
                    )
                )

            print("\nSignals:")
            print(
                candidate.get(
                    "redrob_signals",
                    {}
                )
            )

            print("\n" + "=" * 80)

            break