import json
import pandas as pd

rows = []

with open("data/raw/candidates.jsonl", "r", encoding="utf-8") as f:

    for line in f:

        c = json.loads(line)

        s = c["redrob_signals"]

        rows.append({
            "open_to_work": s["open_to_work_flag"],
            "response_rate": s["recruiter_response_rate"],
            "github_score": s["github_activity_score"],
            "saved": s["saved_by_recruiters_30d"],
            "interview_rate": s["interview_completion_rate"],
            "notice": s["notice_period_days"]
        })

df = pd.DataFrame(rows)

print(df.describe())

print("\nOpen To Work:")
print(df["open_to_work"].value_counts())