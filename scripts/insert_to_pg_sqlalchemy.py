# scripts/insert_to_pg_sqlalchemy.py
import pandas as pd
from sqlalchemy import create_engine, text
import os

CSV_PATH = "D:/kifiya AI/bank-app-review/data/reviews_clean.csv"
DB_URL = "postgresql+psycopg2://analyst:7600@localhost:5432/bank_reviews"

def get_bank_id_map(engine):
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT bank_id, bank_name FROM banks")).fetchall()
    return {r.bank_name: r.bank_id for r in rows}

def main():
    df = pd.read_csv(CSV_PATH)

    # Ensure columns: review, rating, date, bank, source
    df = df.rename(columns={
        "content":"review", "score":"rating", "at":"date"  # if leftover raw names
    }, errors='ignore')

    # Convert date to YYYY-MM-DD
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date

    engine = create_engine(DB_URL, echo=False)

    # Map bank_name -> bank_id
    bank_map = get_bank_id_map(engine)
    df['bank_id'] = df['bank'].map(bank_map)

    # If any bank_id missing, print and exit
    missing = df[df['bank_id'].isna()]['bank'].unique()
    if len(missing) > 0:
        print("ERROR: these banks are missing in banks table:", missing)
        return

    # Select and rename to match reviews table
    insert_df = df.rename(columns={
        'review': 'review_text',
        'rating': 'rating',
        'date': 'review_date',
        'source': 'source'
    })[['bank_id','review_text','rating','review_date','source']]

    # Add placeholders for sentiment if not present
    if 'sentiment_label' not in insert_df.columns:
        insert_df['sentiment_label'] = None
    if 'sentiment_score' not in insert_df.columns:
        insert_df['sentiment_score'] = None

    # Use pandas to_sql in chunks
    insert_df.to_sql('reviews', engine, if_exists='append', index=False, method='multi', chunksize=500)
    print("Insert complete.")

if __name__ == '__main__':
    main()
