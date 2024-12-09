import streamlit as st
import fetch
import summary_
import suggested_keywords
import nltk

# Download NLTK resources once
# nltk.download('stopwords')
# nltk.download('punkt')

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []


def main():
    st.title("Quick Search")
    st.sidebar.header("Search Parameters")

    # Define form to capture query and parameters
    with st.sidebar.form("search_form"):
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
        search_button = st.form_submit_button("**Search**")

    if search_button and input_query:
        st.session_state.input_query = input_query
        # Fetch URLs related to the input query
        article_links = fetch.fetch_urls(input_query, start=0, stop=2)
        print("Searched", article_links)

        article_content = ""
        for link in article_links:
            try:
                article_content += fetch.extract_content(link)["content"]
            except Exception as e:
                print("Error@37-app:", e)

        summary = summary_.generate_summary(article_content, max_token_limit, language)
        # print(summary)
        st.session_state.summary = summary
        st.session_state.messages.append(summary)

    for i in st.session_state.messages:
        st.write(i)

    with st.form("message_form"):
        prompt = st.text_area("What would you like to ask?", key="user_input")
        if st.form_submit_button("Send"):
            if prompt:
                st.session_state.messages.append(f"You: {prompt}")
                ai_response = summary_.generate_resp(
                    st.session_state.input_query, st.session_state.messages, prompt
                )
                st.session_state.messages.append(f"AI: {ai_response}")
                st.rerun()

    st.header("Things You Might Like")

    if "summary" in st.session_state and "input_query" in st.session_state:
        if not "suggested" in st.session_state:
            st.session_state.suggested = suggested_keywords.get_suggested(
                st.session_state.input_query, st.session_state.summary
            )
            st.rerun()

    if "suggested" in st.session_state:
        for link in st.session_state.suggested:
            print(link)
            obj = fetch.extract_content(link)
            if not obj["status"]:
                continue
            title = obj["title"]

            st.subheader(title)
            st.write(link)


if __name__ == "__main__":
    main()
