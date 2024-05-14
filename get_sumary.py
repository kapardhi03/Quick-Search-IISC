from openai import OpenAI


def generate_summary(full_text , max_token_limit,language):
    if language != "English": max_token_limit = int(max_token_limit * 3) 
    prompt = f"give me a comnbined summary of these articles in {language}:\n"+full_text

    client = OpenAI(api_key = "sk-proj-HE0HHifzC3W7XTg7D1SOT3BlbkFJ74NFhtMa8PEMA7UUnCSD")

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],max_tokens= max_token_limit
    )

    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content

