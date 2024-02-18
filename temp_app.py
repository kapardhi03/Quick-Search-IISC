import streamlit as st
from fectch_and_extract import extract_text, fetch_articles
from get_sumary import generate_summary
from key_world_url import get_key_links
from goose3 import Goose

g = Goose()
SEARCH_RESULTS_START = 1
SEARCH_RESULTS_STOP = 3

def main():
    st.set_page_config(layout="wide")
    st.title("Quick Search")

    # Sidebar
    st.sidebar.header("Search Parameters")
    input_query = st.sidebar.text_area("**Search here:**", height=100)
    max_token_limit = st.sidebar.number_input("**Adjust length[Maximum words]**", min_value=50, max_value=500, value=200, step=10)
    language = st.sidebar.selectbox("**Select Language**", ["English", "Kannada", "Hindi", "Telugu"])

    if st.sidebar.button("**Search**"):
        st.empty()

        articles = fetch_articles(input_query, start=SEARCH_RESULTS_START, stop=SEARCH_RESULTS_STOP)
        articles = articles[:4]

        result = ""
        for article in articles:
            try:
                result += extract_text(article)["content"]
            except Exception as e:
                print("Error:", e)

        st.header("Summary")
        summary = generate_summary(result, max_token_limit, language=language)
        st.write(summary)

        st.header("Things You Might Like")

        urls = get_key_links(user_query=input_query, summary=summary)

        for key in urls:
            
            title = g.extract(urls[key][0]).title
            if title == "": continue
            st.subheader(title)
            st.write(urls[key][0])
            st.write("---")

if __name__ == "__main__":
    main()
