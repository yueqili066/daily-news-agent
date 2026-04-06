import os
from google import genai

def run_research_agent():
    # 1. Initialize the 2026 Client
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    # 2. Define your "Source Portfolio"
    # You can add or remove any URLs here
    target_sources = [
        "https://endpts.com",             # Biotech Deep Dives
        "https://www.fiercebiotech.com",  # Industry M&A
        "https://www.biopharmadive.com",  # Regulatory News
        "https://www.reuters.com/business/healthcare-pharmaceuticals/", # General Pharma
        "https://www.statnews.com"        # Clinical Trials
    ]

    # 3. The "Intelligence Command"
    # We tell the agent exactly what to look for across these sites
    research_query = f"""
    Perform a high-level scan of the following websites: {', '.join(target_sources)}.
    
    Extract and summarize:
    1. Any M&A deals announced in the last 24 hours.
    2. Any new FDA/NMPA submissions or approvals.
    3. Significant geopolitical shifts affecting tech or drug supply chains.
    
    Format the output as a '9:00 AM Executive Briefing'. 
    If a site is behind a heavy paywall, move to the next one.
    """

    print(f"🚀 Agent is now researching {len(target_sources)} sources...")

    try:
        # We use the 'google_search' tool which allows the agent 
        # to effectively "browse" the live web in 2026
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            config={
                'tools': [{'google_search': {}}],
                'system_instruction': "You are a professional research agent for a top-tier consulting firm."
            },
            contents=research_query
        )
        
        print("\n--- 🚀 MULTI-SOURCE DAILY SUMMARY ---")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Research Error: {e}")

if __name__ == "__main__":
    run_research_agent()
