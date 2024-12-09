import yake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import fetch


# Default parameters for YAKE keyword extraction
language = "en"
max_ngram_size = 2
deduplication_threshold = 0.9
deduplication_algo = "seqm"
windowSize = 1


def scale_value(string, min_new=2, max_new=10):
    value = len(string)
    min_old = min_new
    max_old = max_new
    value_scaled = ((value - min_old) / (max_old - min_old)) * (
        max_new - min_new
    ) + min_new

    return round(value_scaled * 0.003)


def get_keywords(summary):
    tokens = word_tokenize(summary)

    stop_words = stopwords.words("english")
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    filtered_text = " ".join(filtered_tokens)

    # Initialize YAKE keyword extractor
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        dedupFunc=deduplication_algo,
        windowsSize=windowSize,
        top=5,
        features=None,
        # stopwords=True,
    )

    keywords = custom_kw_extractor.extract_keywords(filtered_text)

    return keywords


def get_suggested(query, summary):
    # print("Getting suggested")
    keywords = get_keywords(summary.replace("\n", ". "))
    # print("Key words", keywords)

    # Fetch articles related to each keyword
    suggested = []
    x = 5
    start = 1
    for key_word, score in keywords:
        # print(key_word)
        try:
            articles = fetch.fetch_urls(
                query + " " + key_word, start=start, stop=start + 2
            )
            # print(articles)
            suggested.extend(articles)
            start += 1
        except:
            continue

    return list(set(suggested))
