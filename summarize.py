import os
import google.generativeai as genai

def summarize_content(content):
    if not content:
        return "No content to summarize."

    # Gemini API の設定
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")  # モデルは適宜変更

    try:
        # プロンプトで要約を指示
        prompt = f"Summarize the following content in 100 words or less:\n\n{content}"
        response = model.generate_content(prompt)
        summary = response.text
        return summary if summary else "Failed to generate summary."

    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Error summarizing content."
