# from openai import OpenAI, APIError
# client = OpenAI(api_key="sk-ECmCcuNnc7W8wnl1yxNgu9jNBDnoIMC1ZFprM4c71YT3BlbkFJwDdr-s6TMR-2Lr0FfuVljRswQdtKoJnlVuaIff0pkA")

# def generate_summary(full_text, max_token_limit, language):
#     if language != "English":
#         max_token_limit = int(max_token_limit * 3)

#     prompt = f"give me a combined summary of these articles in {language}:\n" + full_text

#     try:
#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=max_token_limit
#         )

#         return completion.choices[0].message.content

#     except APIError as e:
#         if e.code == "invalid_api_key":
#             raise Exception("API limit expired or not supported by OpenAI")
#         else:
#             raise e


# def get_response(prompt):
#     try:
#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#         )

#         return completion.choices[0].message.content

#     except APIError as e:
#         if e.code == "invalid_api_key":
#             raise Exception("API limit expired or not supported by OpenAI")
#         else:
#             raise e





from openai import OpenAI, APIError
import streamlit as st
from typing import Dict
import re

def format_summary_for_streamlit(text: str) -> str:
    """Format the summary text with proper markdown for Streamlit display"""
    # Add emoji indicators for different sections
    sections = text.split('\n\n')
    formatted_sections = []
    
    for section in sections:
        if section.strip():
            # Add bullet points if line starts with dash or asterisk
            section = re.sub(r'^[•\-\*]\s*', '• ', section.strip(), flags=re.MULTILINE)
            formatted_sections.append(section)
    
    return '\n\n'.join(formatted_sections)

def generate_summary(full_text: str, max_token_limit: int, language: str = "English") -> Dict:
    """
    Generate a well-structured summary optimized for Streamlit display
    
    Args:
        full_text: Text to summarize
        max_token_limit: Maximum tokens for response
        language: Target language
    
    Returns:
        Dictionary containing formatted summary sections
    """
    if language != "English":
        max_token_limit = int(max_token_limit * 1.5)

    system_prompt = """You are an expert summarizer who creates engaging, well-structured summaries.
Your summaries should be:
1. Easy to read and understand
2. Well-organized with clear sections
3. Highlighted with key information
4. Engaging for readers"""

    user_prompt = f"""Provide a comprehensive summary in {language} with the following structure:

📝 MAIN SUMMARY
[Provide a clear 2-3 sentence overview]

🎯 KEY POINTS
• [Key point 1]
• [Key point 2]
• [Key point 3]

💡 INSIGHTS
• [Important insight or takeaway]
• [Any significant trends or patterns]

Text to summarize:
{full_text}

Format the response with appropriate emoji indicators and bullet points."""

    try:
        # client = OpenAI(api_key="sk-ECmCcuNnc7W8wnl1yxNgu9jNBDnoIMC1ZFprM4c71YT3BlbkFJwDdr-s6TMR-2Lr0FfuVljRswQdtKoJnlVuaIff0pkA")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_token_limit,
            temperature=0.7,
            presence_penalty=0.6,
            frequency_penalty=0.3
        )

        summary = completion.choices[0].message.content
        formatted_summary = format_summary_for_streamlit(summary)

        # Create expandable sections using Streamlit components
        st.markdown("### 📌 Summary Overview")
        main_summary = formatted_summary.split("🎯")[0].strip()
        st.write(main_summary)

        with st.expander("🎯 Key Points & Insights"):
            remaining_content = "🎯" + formatted_summary.split("🎯")[1]
            st.markdown(remaining_content)

        # Add interactive elements
        if st.checkbox("Show Word Count"):
            word_count = len(formatted_summary.split())
            st.info(f"Summary contains {word_count} words")

        return formatted_summary

    except APIError as e:
        if e.code == "invalid_api_key":
            st.error("API key is invalid or has expired")
        else:
            st.error(f"OpenAI API error: {str(e)}")
        raise Exception("API error occurred")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        raise e