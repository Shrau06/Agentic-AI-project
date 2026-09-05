from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=API_KEY)


def get_news(query, page_size=5):
    """
    Fetch relevant news related to a company.
    """

    try:

        response = newsapi.get_everything(
            q=f'"{query}"',
            language="en",
            sort_by="publishedAt",
            page_size=20
        )

        articles = response.get("articles", [])

        filtered_articles = []

        for article in articles:

            title = article.get("title", "")
            description = article.get("description", "")

            text = f"{title} {description}".lower()

            if query.lower() in text:
                filtered_articles.append(article)

        if filtered_articles:
            return filtered_articles[:page_size]

        return articles[:page_size]

    except Exception as e:
        print("Error:", e)
        return []