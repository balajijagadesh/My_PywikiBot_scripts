import requests
import json
from datetime import datetime, timedelta

# File containing article names
file_path = "articles_eng.txt"

# Dates for the past 30 days
end_date = datetime.today()
start_date = end_date - timedelta(days=30)
start_date_str = start_date.strftime("%Y%m%d")
end_date_str = end_date.strftime("%Y%m%d")

# Define Wikimedia API URL template (change the language as per requirement)
url_template = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{}/daily/{}/{}"

# User-Agent header for Wikimedia API
headers = {
    "User-Agent": "Custom Script for Pageviews Analysis (User:Balajijagadesh)"
}

# Read articles from file
with open(file_path, "r", encoding="utf-8") as file:
    articles = [line.strip() for line in file]

# Fetch pageview data
results = []
for article in articles:
    encoded_article = requests.utils.quote(article)
    url = url_template.format(encoded_article, start_date_str, end_date_str)
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            total_views = sum(item['views'] for item in data['items'])
            results.append((article, total_views))
        else:
            print(f"Error fetching data for {article}: {response.status_code}")
            results.append((article, 0))
    except Exception as e:
        print(f"Exception fetching data for {article}: {e}")
        results.append((article, 0))

# Print results in wikitable format
wikitable = "{| class='wikitable'\n! Article Name\n! Pageviews\n"
for article, views in results:
    wikitable += f"|-\n| {article}\n| {views}\n"
wikitable += "|}"
print(wikitable)
