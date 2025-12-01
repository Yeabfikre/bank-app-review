## 🚀 Customer Experience Analytics for Fintech Apps

**10 Academy: Artificial Intelligence Mastery - Week 2 Challenge**

### 🎯 Project Overview & Business Objective

This project, conducted on behalf of **Omega Consultancy**, focuses on analyzing customer satisfaction with mobile banking applications from three major Ethiopian banks: **Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank**.

The core objective is to leverage Data Engineering and Natural Language Processing (NLP) to transform unstructured Google Play Store reviews into actionable business insights.

| Metric | Goal |
| :--- | :--- |
| **Sentiment Analysis** | Quantify the tone (Positive/Negative/Neutral) of each review. |
| **Thematic Extraction** | Identify core pain points (e.g., "UI," "Bugs," "Speed") and satisfaction drivers. |
| **Data Engineering** | Store all cleaned and analyzed data in a robust PostgreSQL database. |
| **Deliverable** | Provide a final report with recommendations to improve customer retention and app feature development. |

-----

### 🛠️ Methodology & Technical Stack

| Area | Tool/Technology | Purpose |
| :--- | :--- | :--- |
| **Data Collection** | `google-play-scraper` | Fetching raw user reviews (\>1,200 total). |
| **Sentiment NLP** | Hugging Face `transformers` (e.g., DistilBERT) | High-accuracy sentiment labeling. |
| **Thematic NLP** | `scikit-learn` (TF-IDF/N-grams) | Extracting keywords and grouping into themes. |
| **Data Storage** | PostgreSQL (v15+) | Structured database for querying and reporting. |
| **Programming** | Python (`pandas`, `psycopg2`, `SQLAlchemy`) | Orchestration, ETL, and data manipulation. |
| **Version Control** | Git / GitHub | Code management and CI/CD workflow. |

-----

### 📂 Repository Structure

The project follows a standard Data Science/Data Engineering structure:

```text
.
├── data/
│   ├── raw/
│   ├── clean/            # reviews_clean.csv (after deduplication/date norm)
│   └── processed/        # reviews_sentiment.csv (after NLP)
├── notebooks/            # Jupyter notebooks for EDA and visualization
├── outputs/
│   └── plots/            # Saved PNG/JPG files of all visualizations
├── reports/              # Final insights.md (or final_report.pdf)
├── scripts/
│   ├── scrape.py
│   ├── insert_to_pg_sqlalchemy.py  # OR insert_to_pg_copy.py
│   └── top_keywords.py   # Analysis script
├── sql/
│   ├── schema.sql        # Primary DDL for DB structure
│   └── schema_dump.sql   # Dumped schema (for verification)
├── .gitignore
├── README.md
└── requirements.txt
```

-----

### ⚙️ Setup and Execution Guide

#### 1\. Environment Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Yeabfikre/bank-app-reviews-week2.git
    cd bank-app-reviews-week2
    ```
2.  **Create Virtual Environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    .venv\Scripts\activate     # Windows
    ```
3.  **Install Dependencies:** (Ensure you have all packages listed in `requirements.txt`)
    ```bash
    pip install -r requirements.txt
    ```

#### 2\. TASK 1 & 2: Data Collection and NLP Analysis

1.  **Data Collection (Scraping):**
      * Find the current App IDs for CBE, BOA, and Dashen.
      * Run `scripts/scrape.py` to fetch data and save it to `data/raw/`.
2.  **Preprocessing & Sentiment:**
      * Run your preprocessing script to clean text, handle duplicates, and normalize dates. Save to `data/clean/reviews_clean.csv`.
      * Run your sentiment script (using Hugging Face `transformers`) to add `sentiment_label` and `sentiment_score` columns. Save to `data/processed/reviews_sentiment.csv`.

#### 3\. TASK 3: Database Engineering (PostgreSQL)

The goal is to load the data into the `bank_reviews` database using the `analyst` user.

1.  **Database Setup (Choose one):**
      * **Docker (Recommended):** Run the container, which automatically creates the DB/User:
        ```bash
        docker run --name bank_reviews_pg -e POSTGRES_PASSWORD=strongpassword -e POSTGRES_USER=analyst -e POSTGRES_DB=bank_reviews -p 5432:5432 -d postgres:15
        ```
      * **Native Install:** Create the database and user manually via `psql`.
2.  **Apply Schema (DDL):**
      * The schema is defined in `sql/schema.sql`.
      * Execute the DDL to create the `banks` and `reviews` tables:
        ```bash
        psql -U analyst -d bank_reviews -f sql/schema.sql
        ```
3.  **Seed Banks Table:**
      * Insert the three bank names into the `banks` table to establish the foreign key relationship:
        ```bash
        psql -U analyst -d bank_reviews -c "INSERT INTO banks (bank_name, app_name) VALUES ('CBE', 'com.cbe.mobile'), ('BOA', 'com.boa.app'), ('Dashen', 'com.dashenbank.app') ON CONFLICT (bank_name) DO NOTHING;"
        ```
4.  **Insert Processed Data (ETL):**
      * Execute the Python script to map bank names to `bank_id` and insert the data:
        ```bash
        python scripts/insert_to_pg_sqlalchemy.py
        # OR: python scripts/insert_to_pg_copy.py for large datasets
        ```
5.  **Verification:**
      * Verify the data count: `psql -U analyst -d bank_reviews -c "SELECT COUNT(*) FROM reviews;"`
6.  **Commit Schema:**
      * Dump the schema and commit both schema files:
        ```bash
        pg_dump -U analyst -d bank_reviews -s > sql/schema_dump.sql
        git commit -m "chore(db): add schema and seed for banks + reviews"
        ```

#### 4\. TASK 4: Insights & Reporting

1.  **Analysis Execution:** Run the scripts and notebooks (e.g., `notebooks/plots_sentiment.py`, `scripts/top_keywords.py`) to generate the required visualizations.
2.  **Visuals:** Ensure 3–5 high-quality PNG plots are saved in `outputs/plots/`. Key charts include:
      * Weekly Sentiment Trend (multi-line plot).
      * Rating Distribution (histogram/bar chart).
      * Top 10 Negative Keywords per Bank (bar chart).
3.  **Report Write-up:** Compile all findings, visualizations, and actionable recommendations into a final report (`reports/insights.md` or PDF).

-----

 
