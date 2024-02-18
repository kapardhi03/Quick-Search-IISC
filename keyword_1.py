import nltk
# nltk.download('stopwords')
import yake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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
    # print(round(value_scaled * 0.0029))
    return round(value_scaled * 0.003)


def get_key_words(summary):
    tokens = word_tokenize(summary)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    filtered_text = " ".join(filtered_tokens)

    # Use YAKE with the filtered text
    custom_kw_extractor = yake.KeywordExtractor(
        lan=language,
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        dedupFunc=deduplication_algo,
        windowsSize=windowSize,
        # top=scale_value(summary),
        top=5,
        features=None,
        # stopwords=True,
    )
    keywords = custom_kw_extractor.extract_keywords(filtered_text)

    return keywords
