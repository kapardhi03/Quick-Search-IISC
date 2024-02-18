import certifi
from googlesearch import search
from goose3 import Goose

def extract_text(article_url):
    g = Goose()
    try:
        article = g.extract(article_url)
        if article.cleaned_text is not "" and article.title is not ""  : return {"content": article.cleaned_text, "title": article.title}
    except Exception as e:
        print(f"Error extracting text from article: {e}")
        return {"content": "", "title": ""}

def fetch_articles(user_query, start=1, stop=2):
    articles = []
    try:
        for url in search(user_query, start=start, stop=stop):
            articles.append(url)
        
    except Exception as e:
        print(f"Error fetching articles: {e}")
    return articles
