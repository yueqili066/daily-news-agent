import os
import requests
import feedparser
import google.generativeai as genai

def run_agent():
    # 1. Setup Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in Secrets")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash-preview')

    # 2. Fetch Tech & Geopolitics (GNews)
    gnews_key = os.environ.get("GNEWS_API_KEY")
    gnews_articles = []
    if gnews_key:
        try:
            url = f"https://gnews.io/api/v4/search?q=geopolitics+OR+technology&token={gnews_key}&lang=en&max=5"
            response = requests.get(url, timeout=10)
            gnews_articles = response.json().get('articles', [])
        except Exception as e:
            print(f"GNews Error: {e}")

    # 3. Fetch Biotech/Pharma (RSS)
    rss_urls = [
        "https://www.fiercebiotech.com/biotech/rss",
        "https://www.biopharmadive.com/feed/"
    ]
    industry_news = ""
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                industry_news += f"- {entry.title}: {entry.summary[:200]}...\n"
        except Exception as e:
            print(f"RSS Error for {url}: {e}")

    # 4. Generate Summary
    combined_content = f"MAINSTREAM NEWS:\n{gnews_articles}\n\nINDUSTRY NEWS:\n{industry_news}"
    
    prompt = f"""
    Role: Senior Industry Intelligence Analyst
    Task: 9:00 AM Executive Briefing.
    Context: {combined_content}
    
    Instructions:
    1. Highlight M&A deals and FDA/NMPA submissions in Biotech.
    2. Summarize key Tech/Geopolitical shifts.
    3. Use bullet points. Be concise.
    """

    try:
        response = model.generate_content(prompt)
        print("--- DAILY SUMMARY START ---")
        print(response.text)
        print("--- DAILY SUMMARY END ---")
    except Exception as e:
        print(f"Gemini Error: {e}")

if __name__ == "__main__":
    run_agent()
