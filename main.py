import os
import requests
import feedparser
import google.generativeai as genai

def run_agent():
    # 1. Setup API Key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in Secrets")
        return
    
    genai.configure(api_key=api_key)

    # --- DEBUG STEP: List available models to the log ---
    print("Checking available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Available Model: {m.name}")
    except Exception as e:
        print(f"Could not list models: {e}")

    # 2. Initialize Model (Using 2026 standard name)
    try:
        # Try the most stable 2026 version
        model = genai.GenerativeModel('gemini-3-flash-preview')
    except Exception:
        # Fallback to the latest stable version if preview is unavailable
        model = genai.GenerativeModel('gemini-2.5-flash')

    # 3. Fetch News (GNews + RSS)
    gnews_key = os.environ.get("GNEWS_API_KEY")
    industry_news = ""
    
    # Fetch Biotech/Pharma via RSS (High reliability)
    rss_urls = ["https://www.fiercebiotech.com/biotech/rss", "https://www.biopharmadive.com/feed/"]
    for url in rss_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            industry_news += f"- {entry.title}\n"

    # 4. Generate the Summary
    prompt = f"""
    Role: Senior Industry Analyst
    Task: Daily 9:00 AM Briefing.
    Context: {industry_news}
    Instructions: Identify any M&A deals or biotech submissions. Be concise.
    """

    try:
        response = model.generate_content(prompt)
        print("\n🚀 --- DAILY SUMMARY --- 🚀\n")
        print(response.text)
    except Exception as e:
        print(f"❌ AI Generation Error: {e}")

if __name__ == "__main__":
    run_agent()
