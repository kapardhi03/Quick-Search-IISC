from fectch_and_extract import   fetch_articles
from keyword_1 import get_key_words

def get_key_links(user_query,summary):
    keywords = get_key_words(summary.replace("\n", ". "))

    urls = {}
    for key, score in keywords:
        urls[user_query +" "+ key] = fetch_articles(user_query + " " + key, 0, 1)
        
    for key in urls:
        print(key, urls[key])
    return urls


