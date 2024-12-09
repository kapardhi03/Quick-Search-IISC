import streamlit as st
import fetch
import summary_
import suggested_keywords
import faiss
from dotenv import load_dotenv
import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

import tiktoken

def find_max_text_length(text, model="gpt-3.5-turbo", token_limit=15000):
    encoding = tiktoken.encoding_for_model(model)

    def count_tokens(subtext):
        return len(encoding.encode(subtext))

    low, high = 0, len(text)
    best_fit_length = 0

    while low <= high:
        mid = (low + high) // 2
        substring = text[:mid]
        token_count = count_tokens(substring)

        if token_count <= token_limit:
            best_fit_length = mid
            low = mid + 1
        else:
            high = mid - 1

    return text[:best_fit_length]
 

load_dotenv()

def create_chunks(text, chunk_size=2000):
    return [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]


def main():
    st.title("Quick Search")
    st.sidebar.header("Search Parameters")

    with st.sidebar:
        input_query = st.text_area("**Search here:**", height=100)
        max_token_limit = st.number_input(
            "**Adjust length (Maximum words)**",
            min_value=50,
            max_value=500,
            value=200,
            step=10,
        )
        language = st.selectbox(
            "**Select Language**", ["English", "Kannada", "Hindi", "Telugu"]
        )
        if input_query:
            search_button = st.button("**Search**")
            if search_button:
                st.session_state.input_query = input_query
                st.session_state.show = True
                if "article_links" not in st.session_state:
                    article_links = fetch.fetch_urls(input_query, start=0, stop=3)
                    st.session_state["article_links"] = article_links
                else:
                    article_links = st.session_state["article_links"]

                article_content = ""
                for link in article_links:
                    try:
                        article_content += fetch.extract_content(link)["content"]
                    except Exception as e:
                        print("Error@35-app:", e)

                if "index" not in st.session_state or st.session_state.index is None:
                    chunks = create_chunks(article_content)
                    chunk_vectors = summary_.get_embeddings(chunks)
                    dimension = chunk_vectors.shape[1]
                    index_ = faiss.IndexFlatL2(dimension)
                    index_.add(chunk_vectors)
                    st.session_state["index"] = index_
                    st.session_state["chunks"] = chunks

                summary = summary_.generate_summary(
                    find_max_text_length(article_content), max_token_limit, language
                )
                st.session_state["summary"] = summary

                if len(st.session_state.messages) == 0:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": summary}
                    )

    if st.session_state.show:
        tab1, tab2 = st.tabs(["Ask anything", "More like this"])
        with tab1:

            for message in st.session_state.messages:
                with st.chat_message(
                    message["role"],
                    avatar="🧑‍💻" if message["role"] == "user" else "🤖",
                ):
                    st.markdown(message["content"])

            # Chat input
            if prompt := st.chat_input("What would you like to ask?"):
                # User message
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                # Assistant's response
                with st.spinner("Assistant is thinking..."):
                    lyra_response = summary_.generate_resp(
                        st.session_state.input_query,
                        st.session_state.index,
                        prompt,
                        st.session_state.chunks,
                    )
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(lyra_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": lyra_response}
                )

        with tab2:
            if "suggested" not in st.session_state or st.session_state.suggested is None:
                session_state = suggested_keywords.get_suggested(
                    st.session_state.input_query, st.session_state.summary
                )
                suggested = []
                for link in session_state:
                    obj = fetch.extract_content(link)
                    if not obj["status"]:
                        continue
                    title = obj["title"]
                    suggested.append((title, link))
                    
                
                st.session_state.suggested = suggested
            
            if "suggested" in st.session_state:
                for title, link in st.session_state.suggested:
                    st.subheader(title)
                    st.write(link)



if __name__ == "__main__":
    # Initialize session state for authentication status
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show" not in st.session_state:
        st.session_state.show = False
    if "index" not in st.session_state:
        st.session_state.index = None
    if "chunks" not in st.session_state:
        st.session_state.chunks = None
    if "suggested" not in st.session_state:
        st.session_state.suggested = None

    main()
