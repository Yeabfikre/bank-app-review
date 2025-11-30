from google_play_scraper import Sort, reviews
import pandas as pd

APP_PACKAGES = {
    'CBE': 'com.combanketh.mobilebanking',
    'BOA': 'com.boa.boaMobileBanking',
    'Dashen': 'com.dashen.dashensuperapp'
}

def scrape_reviews(bank_name, app_id, count=600): 
    print(f"Scraping {bank_name}...")
    result, _ = reviews(
        app_id,
        lang='en', 
        country='us', # Country
        sort=Sort.NEWEST, # Get latest reviews
        count=count
    )
    df = pd.DataFrame(result)
    df['bank'] = bank_name
    return df[['content', 'score', 'at', 'bank', 'userName']] # Keep relevant columns

all_reviews = []
for bank, app_id in APP_PACKAGES.items():
    df = scrape_reviews(bank, app_id)
    all_reviews.append(df)

final_df = pd.concat(all_reviews, ignore_index=True)
final_df.to_csv('D:/kifiya AI/bank-app-review/data/raw_reviews.csv', index=False)
print("Scraping Complete!")