import os
import requests
import feedparser # You'll need to install this
import google.generativeai as genai

# 1. Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Fetch Tech & Geopolitics from GNews (API)
gnews_url = f"https://gnews.io/api/v4/search?q=geopolitics+OR+technology&token={os.environ['GNEWS_API_KEY']}&lang=en&max=5"
gnews_data = requests.get(gnews_url).json().get('articles', [])

# 3. Fetch Biotech/Pharma from RSS (No API Key needed!)
# These are the "Gold Standard" feeds for Pharma M&A
rss_urls = [
    "https://www.fiercebiotech.com/biotech/rss",
    "https://www.biopharmadive.com/feed/"
]

industry_news = ""
for url in rss_urls:
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]: # Take top 5 from each
        industry_news += f"- {entry.title}: {entry.summary}\n"

# 4. The Agent Prompt
combined_news = f"MAINSTREAM:\n{gnews_data}\n\nINDUSTRY:\n{industry_news}"

prompt = f"""
Role: Senior Industry Intelligence Analyst
Task: Provide a 9:00 AM executive briefing.
Content: {combined_news}

Instructions:
1. Identify any M&A deals or FDA/NMPA submissions in the Biotech section.
2. Summarize key Tech/Geopolitical shifts.
3. Tone: Professional, concise, data-driven.
"""

summary = model.generate_content(prompt)
print(summary.text)
