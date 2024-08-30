import pandas as pd

def process_news(data):
    news = []
    for article in data["articles"]:
        news.append({
            "title": article["title"],
            "description": article["description"],
            "url": article["url"],
            "urlToImage": article["urlToImage"],
            "publishedAt": pd.to_datetime(article["publishedAt"])
        })
    return pd.DataFrame(news)