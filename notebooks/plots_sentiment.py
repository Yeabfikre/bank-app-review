# notebooks/plots_sentiment.py
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('D:/kifiya AI/bank-app-review/data/reviews_with_sentiment.csv')
df['review_date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['review_date'])
df['week'] = df['review_date'].dt.to_period('W').apply(lambda r: r.start_time)

for bank in df['bank'].unique():
    g = df[df['bank']==bank].groupby('week')['sentiment_score'].mean()
    plt.plot(g.index, g.values, label=bank)

plt.legend()
plt.title('Weekly average sentiment score by bank')
plt.xlabel('Week')
plt.ylabel('Mean sentiment score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/plots/sentiment_trend.png')



import seaborn as sns
import matplotlib.pyplot as plt
df = pd.read_csv('D:/kifiya AI/bank-app-review/data/reviews_with_sentiment.csv')

for bank in df['bank'].unique():
    sns.histplot(df[df['bank']==bank]['rating'], kde=False, bins=5)
    plt.title(f'Rating distribution for {bank}')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.savefig(f'outputs/plots/rating_dist_{bank}.png')
    plt.clf()
