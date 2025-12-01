import pandas as pd

df = pd.read_csv("D:/kifiya AI/bank-app-review/data/reviews_with_themes.csv")

print("\n===== KPI CHECKS =====\n")

# 1. Sentiment completion
sentiment_missing = df["sentiment_label"].isna().mean()
print(f"Sentiment missing: {sentiment_missing:.2%}")
if sentiment_missing < 0.10:
    print("PASS: >90% sentiment completed")
else:
    print("FAIL: <90% sentiment")

# 2. Themes per bank
print("\nThemes per bank:")
theme_counts = df.groupby("bank")["theme_cluster"].nunique()
print(theme_counts)

for bank, count in theme_counts.items():
    if count >= 3:
        print(f"PASS: {bank} has >= 3 themes")
    else:
        print(f"FAIL: {bank} has fewer than 3 themes")
