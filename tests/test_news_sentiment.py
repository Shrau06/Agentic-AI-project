from tools.news_tool import get_news
from sentiment.sentiment_analyzer import analyze_sentiment

articles = get_news("Microsoft")

for article in articles:

    title = article["title"]

    sentiment = analyze_sentiment(title)

    print("Title:", title)
    print("Sentiment:", sentiment)

    print("-" * 50)