import streamlit as st
from goose3 import Goose
from typing import List, Dict, Any
import time
from fectch_and_extract import extract_text, fetch_articles
from get_sumary import generate_summary
from key_world_url import get_key_links

# Constants
SEARCH_RESULTS_START = 1
SEARCH_RESULTS_STOP = 3
MAX_ARTICLES = 4

class SearchApp:
    def __init__(self):
        self.goose = Goose()
        self.setup_page_config()
        self.initialize_session_state()

    def setup_page_config(self):
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title="Quick Search & Summarize",
            page_icon="🔍",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'search_history' not in st.session_state:
            st.session_state.search_history = []

    def render_sidebar(self) -> tuple:
        """Render sidebar elements and return input values"""
        st.sidebar.title("Quick Search ")
        
        input_query = st.sidebar.text_area(
            "**Enter your search query:**",
            height=100,
            placeholder="Type your search query here..."
        )
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            max_token_limit = st.number_input(
                "**Max Words**",
                min_value=50,
                max_value=500,
                value=200,
                step=10,
                help="Adjust the length of the summary"
            )
            
        with col2:
            language = st.selectbox(
                "**Language**",
                ["English", "Kannada", "Hindi", "Telugu"],
                help="Select summary language"
            )

        # Add search history
        if st.session_state.search_history:
            st.sidebar.subheader("Recent Searches")
            for query in st.session_state.search_history[-5:]:  # Show last 5 searches
                st.sidebar.text(f"• {query}")

        return input_query, max_token_limit, language

    def process_articles(self, input_query: str) -> str:
        """Fetch and process articles based on search query"""
        with st.spinner("Searching for relevant articles..."):
            articles = fetch_articles(
                input_query,
                start=SEARCH_RESULTS_START,
                stop=SEARCH_RESULTS_STOP
            )[:MAX_ARTICLES]

        combined_text = ""
        for idx, article in enumerate(articles, 1):
            try:
                article_content = extract_text(article)["content"]
                combined_text += article_content + "\n\n"
            except Exception as e:
                st.warning(f"⚠️ Couldn't process article {idx}: {str(e)}")
                continue

        return combined_text

    def display_summary(self, text: str, max_token_limit: int, language: str) -> str:
        """Generate and display the summary"""
        with st.spinner("✍️ Generating summary..."):
            summary = generate_summary(text, max_token_limit, language)
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📝 Summary", "📊 Details"])
            
            with tab1:
                st.markdown(summary)
                
            with tab2:
                st.info(f"📏 Summary length: {len(summary.split())} words")
                st.info(f"🔤 Language: {language}")
                
            return summary

    def display_related_articles(self, input_query: str, summary: str):
        """Display related articles section"""
        with st.spinner("🔗 Finding related articles..."):
            urls = get_key_links(user_query=input_query, summary=summary)
            
            st.header("📚 Related Articles")
            
            for key, url_data in urls.items():
                try:
                    article = self.goose.extract(url=url_data[0])
                    if article.title:
                        with st.expander(f"📰 {article.title}"):
                            st.write(url_data[0])
                            st.caption("Click to read full article")
                except Exception as e:
                    continue

    def handle_user_interaction(self):
        """Handle user input and button interactions"""
        input_query, max_token_limit, language = self.render_sidebar()

        if st.sidebar.button(" **Search**", type="primary", use_container_width=True):
            if not input_query:
                st.error("⚠️ Please enter a search query")
                return

            try:
                # Update search history
                if input_query not in st.session_state.search_history:
                    st.session_state.search_history.append(input_query)
                
                # Main content area
                st.title("Search Results")
                
                # Process articles
                combined_text = self.process_articles(input_query)
                if not combined_text:
                    st.error("❌ No articles found. Please try a different search query.")
                    return

                # Generate and display summary
                summary = self.display_summary(combined_text, max_token_limit, language)

                # Display related articles
                self.display_related_articles(input_query, summary)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.error("Please try again with a different query or check your API key.")

def main():
    """Main application entry point"""
    app = SearchApp()
    app.handle_user_interaction()

if __name__ == "__main__":
    main()