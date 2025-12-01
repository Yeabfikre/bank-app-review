import pandas as pd
import numpy as np

import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

INPUT_PATH = "D:/kifiya AI/bank-app-review/data/reviews_with_sentiment.csv"
OUTPUT_THEMES = "D:/kifiya AI/bank-app-review/data/themes_per_bank.json"
OUTPUT_FINAL = "D:/kifiya AI/bank-app-review/data/reviews_with_themes.csv"

def extract_top_keywords(tfidf, cluster_indices, feature_names, top_n=10):
    """Extract top keywords for a given cluster."""
    cluster_tfidf = tfidf[cluster_indices].mean(axis=0)
    if hasattr(cluster_tfidf, "toarray"):
        cluster_tfidf = cluster_tfidf.toarray()

    cluster_tfidf = np.array(cluster_tfidf).flatten()

    top_indices = cluster_tfidf.argsort()[-top_n:][::-1]
    return [feature_names[i] for i in top_indices]

def run_thematic_analysis():
    df = pd.read_csv(INPUT_PATH)

    themes_output = {}

    print("Loading sentence-transformers model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    for bank in df["bank"].unique():
        print(f"\n=== Processing {bank} ===")
        bank_df = df[df["bank"] == bank].reset_index(drop=True)

        texts = bank_df["review"].astype(str).tolist()

        print("Embedding reviews...")
        embeddings = model.encode(texts, show_progress_bar=True)

        print("Clustering into 3 themes...")
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        bank_df["theme_cluster"] = clusters

        # TF-IDF for keyword extraction
        print("Extracting keywords...")
        vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))
        tfidf_matrix = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()

        bank_themes = []
        for c in range(3):
            cluster_indices = bank_df[bank_df["theme_cluster"] == c].index.tolist()
            keywords = extract_top_keywords(tfidf_matrix, cluster_indices, feature_names)
            example_reviews = bank_df[bank_df["theme_cluster"] == c]["review"].head(3).tolist()

            bank_themes.append({
                "theme_id": c,
                "keywords": keywords,
                "example_reviews": example_reviews,
            })

        themes_output[bank] = bank_themes

    # Save all themes
    print("Merging cluster assignments for all banks...")

    all_banks = []

    for bank in df["bank"].unique():
        bank_df = df[df["bank"] == bank].reset_index(drop=True)
        texts = bank_df["review"].astype(str).tolist()

        # Recompute embeddings and clusters (same as before)
        embeddings = model.encode(texts, show_progress_bar=True)
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(embeddings)

        bank_df["theme_cluster"] = clusters
        all_banks.append(bank_df)

    # Combine all banks into one final DF
    merged = pd.concat(all_banks, ignore_index=True)

    # Save final dataset
    merged.to_csv(OUTPUT_FINAL, index=False)
    print(f"DONE → saved {OUTPUT_FINAL}")


if __name__ == "__main__":
    run_thematic_analysis()
