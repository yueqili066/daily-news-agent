import os
import feedparser
from google import genai

def run_agent():
    # 1. Initialize the 2026 Client
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 2. Fetch Biotech News
    news_text = ""
    feeds = [
        "https://www.fiercebiotech.com/biotech/rss", 
        "https://www.biopharmadive.com/feed/"
    ]
    
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                # We strip HTML tags and limit length for clarity
                news_text += f"HEADLINE: {entry.title}\nSUMMARY: {entry.summary[:200]}\n\n"
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # --- DEBUG: Print what we found to the GitHub log ---
    if not news_text:
        print("⚠️ No news found! Check if the RSS links are working.")
        return
    else:
        print(f"Found {news_text.count('HEADLINE:')} headlines. Sending to AI...")

    # 3. Improved Agent Prompt
    # This tells the AI: "Here is the data, do not ask me for it."
    system_instruction = """
    You are a Senior Industry Intelligence Analyst. 
    I have provided news headlines and summaries below. 
    Your task is to analyze THIS SPECIFIC DATA and provide an executive briefing. 
    Do NOT ask the user for more information. 
    If no M&A is mentioned, simply state 'No major M&A reported today.'
    """

    user_prompt = f"Analyze the following news and provide the executive summary:\n\n{news_text}"

    # 4. Generate content
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        config={'system_instruction': system_instruction},
        contents=user_prompt
    )

    print("\n--- 🚀 DAILY SUMMARY ---")
    print(response.text)

if __name__ == "__main__":
    run_agent()
