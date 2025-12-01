-- sql/schema.sql

CREATE TABLE IF NOT EXISTS banks (
  bank_id SERIAL PRIMARY KEY,
  bank_name TEXT NOT NULL UNIQUE,
  app_name TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
  review_id SERIAL PRIMARY KEY,
  bank_id INTEGER NOT NULL REFERENCES banks(bank_id) ON DELETE CASCADE,
  review_text TEXT NOT NULL,
  rating SMALLINT,
  review_date DATE,
  sentiment_label TEXT,
  sentiment_score REAL,
  source TEXT,
  raw_user_name TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- index to speed lookups by bank
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);
