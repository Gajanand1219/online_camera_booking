
import openai

# Initialize OpenAI client
client = openai.OpenAI(api_key="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")

def chat(user_message):
    if not user_message:
        return {"error": "Message is required"}

    try:
        # Get AI response
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_response = completion.choices[0].message.content
        return {"response": ai_response}
    except Exception as e:
        return {"error": str(e)}

# Example usage
user_message = input("Enter your message: ")
response = chat(user_message)
print(response)
