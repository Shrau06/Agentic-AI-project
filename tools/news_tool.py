import feedparser
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_news(query, page_size=5):
    """
    Fetch relevant company news from Google News RSS.
    """

    try:

        search_query = quote(f'"{query}" stock')

        url = (
            "https://news.google.com/rss/search?"
            f"q={search_query}"
            "&hl=en-IN"
            "&gl=IN"
            "&ceid=IN:en"
        )

        feed = feedparser.parse(url)

        articles = []

        for entry in feed.entries[:page_size]:

            title = entry.get("title", "")
            summary_html = entry.get("description", "")
            summary = BeautifulSoup(summary_html, "html.parser").get_text(" ", strip=True)
            link = entry.get("link", "")
            published = entry.get("published", "")

            articles.append(
                {
                    "title": title,
                    "description": summary,
                    "url": link,
                    "published": published
                }
            )

        return articles

    except Exception as e:
        print("Error:", e)
        return []