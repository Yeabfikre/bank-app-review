import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import os

INPUT_PATH = "D:/kifiya AI/bank-app-review/data/reviews_clean.csv"
OUTPUT_PATH = "D:/kifiya AI/bank-app-review/data/reviews_with_sentiment.csv"

def run_sentiment():
    print("Loading data...")
    df = pd.read_csv(INPUT_PATH)

    # Load HuggingFace model
    print("Loading sentiment model (this may take 10–20 seconds)...")
    nlp = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

    # For saving output
    sentiments = []
    scores = []

    print("Running sentiment analysis...")
    for text in tqdm(df["review"], desc="Processing reviews"):
        text = str(text)[:512]   # truncation to avoid token limit
        result = nlp(text)[0]
        sentiments.append(result["label"])
        scores.append(result["score"])

    df["sentiment_label"] = sentiments
    df["sentiment_score"] = scores

    print(f"Saving to {OUTPUT_PATH} ...")
    df.to_csv(OUTPUT_PATH, index=False)
    print("DONE!")

if __name__ == "__main__":
    run_sentiment()
