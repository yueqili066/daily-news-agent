import os
import requests
import feedparser
import google.generativeai as genai

def run_agent():
    # 1. Setup Gemini (GitHub provides the key from 'Secrets')
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    # 2. Use the CONFIRMED April 2026 model name
    # gemini-1.5 is now retired.
    model = genai.GenerativeModel('gemini-3-flash-preview')

    # 3. Fetch News (Biotech RSS is most reliable)
    industry_news = ""
    rss_urls = ["https://www.fiercebiotech.com/biotech/rss", "https://www.biopharmadive.com/feed/"]
    
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                industry_news += f"- {entry.title}\n"
        except:
            continue

    # 4. Generate the Briefing
    prompt = f"""
    Role: Industry Analyst
    Task: Summarize today's Biotech M&A and tech shifts.
    News: {industry_news}
    Format: Bullet points, professional tone.
    """

    try:
        response = model.generate_content(prompt)
        print("--- 🚀 DAILY BRIEFING ---")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_agent()
