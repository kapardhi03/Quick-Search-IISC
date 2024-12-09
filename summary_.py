from openai import OpenAI
from dotenv import load_dotenv
import os
import faiss
from sentence_transformers import SentenceTransformer

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key="")

def get_embeddings(text, model="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model)
    embeddings = model.encode(text, convert_to_numpy=True)
    return embeddings

def generate_summary(text, max_token_limit, language):
    # Adjust max token limit for non-English language
    if language != "English":
        max_token_limit = int(max_token_limit * 3)

    prompt = (
        f"give me a comnbined summary of these articles in {language} in a readable text format:\n"
        + text
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_token_limit,
    )

    return completion.choices[0].message.content


def generate_resp(input_query, index, prompt, chunks, k=5):
    # Adjust max token limit for non-English language
    # print(messages)
    embed = get_embeddings([input_query])
    D, I = index.search(embed, k)
    messages = []
    for i in I[0]:
        messages.append(chunks[int(i)])
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "\n".join(messages)},
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content
