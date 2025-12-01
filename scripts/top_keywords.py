import pandas as pd
from collections import Counter
import re

df = pd.read_csv('D:/kifiya AI/bank-app-review/data/reviews_with_sentiment.csv')
# negative reviews
neg = df[df['sentiment_label']=='NEGATIVE']
def tokenize(text):
    tokens = re.findall(r'\b[a-z]{3,}\b', str(text).lower())
    tokens = [t for t in tokens if t not in set(['app','bank','mobile'])]
    return tokens

words = Counter()
for t in neg['review'].dropna().astype(str):
    words.update(tokenize(t))
print(words.most_common(30))
