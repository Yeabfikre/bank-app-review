import pandas as pd
import os



INPUT_FILE = "D:/kifiya AI/bank-app-review/data/raw_reviews.csv"
OUTPUT_PATH = "D:/kifiya AI/bank-app-review/data/reviews_clean.csv"

def preprocess():
    df = pd.read_csv(INPUT_FILE)

    df = df.rename(columns={
        "content": "review",
        "score": "rating",
        "at": "date"
    })

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["source"] = "google_play"

    df = df[df["review"].notna()]
    df = df[df["review"].str.strip() != ""]

    df = df.drop_duplicates(subset=["review", "rating", "date", "bank"])

    df.to_csv(OUTPUT_PATH, index=False)
    print("\nSaved:", OUTPUT_PATH)
    print("Rows:", len(df))

if __name__ == "__main__":
    preprocess()