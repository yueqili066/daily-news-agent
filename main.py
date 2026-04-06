import os
import feedparser
from google import genai

def run_agent():
    # 1. Initialize the new 2026 Client
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 2. Fetch Biotech News (RSS is most reliable)
    news_text = ""
    feeds = ["https://www.fiercebiotech.com/biotech/rss", "https://www.biopharmadive.com/feed/"]
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            news_text += f"- {entry.title}\n"

    # 3. Generate content using Gemini 3.1
    # Note: 'gemini-1.5-flash' is GONE. This is the correct 2026 name.
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=f"Summarize these biotech headlines for an executive: {news_text}"
    )

    print("--- 🚀 DAILY SUMMARY ---")
    print(response.text)

if __name__ == "__main__":
    run_agent()
