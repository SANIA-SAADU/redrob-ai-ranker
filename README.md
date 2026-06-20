# Redrob AI Candidate Ranking System

## Problem Statement

Develop a robust AI-based candidate ranking system capable of understanding complex job requirements and intelligently ranking candidates using profile information, career metadata, and behavioral signals.

The system should go beyond keyword filtering and function as an intelligent AI recruiter capable of delivering highly relevant candidate shortlists.

---

## Solution Overview

This project implements a hybrid AI candidate ranking engine that combines:

* Semantic understanding using Sentence Transformers
* Feature-engineered relevance signals
* Behavioral signal integration
* Domain-aware scoring
* Company priors
* Negative profile penalties

Instead of relying on keyword matching, the system captures contextual relevance between job requirements and candidate experience.

---

## Architecture Diagram

![Architecture Diagram](assets/architecture.png)

---

## Core Features

### Deep Job Understanding

The job description is transformed into semantic embeddings using:

* Sentence Transformers (`all-MiniLM-L6-v2`)

This enables understanding of contextual meaning rather than exact words.

Example:

"Recommendation Systems"

can match candidates mentioning:

* retrieval systems
* ranking systems
* embeddings
* semantic search

without exact keyword overlap.

---

### Candidate Intelligence Layer

Candidate information aggregated:

* Headline
* Summary
* Skills
* Career history
* Work descriptions
* Current role
* Experience

---

### Signal Integration

Signals incorporated:

1. Semantic Match Score
2. Retrieval/Search Experience Score
3. Production ML Score
4. Evaluation Metrics Score
5. AI Skills Score
6. Title Score
7. Experience Score
8. Behavioral Score
9. Company Prior Score
10. Negative Profile Penalty

---

## Ranking Formula

Final Score =

0.30 × Semantic Score +

0.25 × Retrieval Score +

0.15 × Title Score +

0.10 × Production Score +

0.05 × Evaluation Score +

0.05 × AI Score +

0.05 × Experience Score +

0.03 × Behavioral Score +

0.02 × Company Score

− Negative Penalty

---

## Pipeline

```text
Candidate Data
      ↓
Text Aggregation
      ↓
Sentence Transformer Embeddings
      ↓
Feature Engineering

        ├── Semantic Match
        ├── Retrieval Score
        ├── Production ML Score
        ├── Evaluation Score
        ├── AI Skill Score
        ├── Experience Score
        ├── Behavioral Score
        ├── Company Prior
        └── Negative Profile Detection

      ↓

Weighted Ranking Engine

      ↓

Top Ranked Candidates

      ↓

Submission CSV
```

---

## Tech Stack

* Python
* Sentence Transformers
* Scikit-learn
* Pandas
* JSON
* Cosine Similarity

---

## Project Structure

```text
redrob-ai-ranker/

├── src/
│   ├── ranker_v2.py
│   ├── ranker_v3.py
│   ├── ranker_v4.py
│   ├── ranker_v5.py
│   ├── ranker_v6.py
│   ├── generate_submission.py
│   └── inspect_candidate.py

├── outputs/
│   ├── top100_v6.csv
│   └── submission.csv

├── assets/
│   └── architecture.png

└── README.md
```

---

## Model Evolution

### V2

* Semantic similarity baseline
* Title matching

### V3

* Added behavioral signals
* Added domain scoring

### V4

* Added retrieval/search expertise features

### V5

* Added production ML signals
* Added evaluation metric signals

### V6

* Added company priors
* Added negative profile penalties
* Optimized feature weighting

---

## Results

The system generated ranked candidate shortlists with explainable reasoning.

Capabilities achieved:

✓ Deep job understanding

✓ Contextual candidate matching

✓ Multi-signal integration

✓ Reduced false positives

✓ Fast candidate retrieval

---

## Key Design Decisions

* Used semantic embeddings instead of keyword matching to improve contextual understanding.
* Prioritized retrieval and search signals because the JD strongly emphasized ranking systems.
* Included production ML signals to identify real-world deployment experience.
* Added evaluation metric signals such as NDCG and MRR.
* Penalized unrelated profiles to reduce noisy candidate matches.

---

## Future Improvements

* Cross-encoder reranking
* Learning-to-rank models
* Dynamic weight optimization
* Recruiter feedback loop
* Online learning

---

## How To Run

Install dependencies:

```bash
pip install pandas
pip install scikit-learn
pip install sentence-transformers
```

Run ranking:

```bash
python src/ranker_v6.py
```

Generate submission:

```bash
python src/generate_submission.py
```

Inspect candidate:

```bash
python src/inspect_candidate.py
```
