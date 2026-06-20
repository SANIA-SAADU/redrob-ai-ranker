import os

print("="*50)
print("Redrob AI Candidate Ranking System")
print("="*50)

print("\nRunning FINAL V6 ranking model...\n")

os.system("python src/ranker_v6.py")

print("\nGenerating submission...\n")

os.system("python src/generate_submission.py")

print("\nDone.")