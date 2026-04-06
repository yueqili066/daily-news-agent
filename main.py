import os
import time
from google import genai

def run_gentle_agent():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    target_sources = [
        "https://endpts.com",
        "https://www.fiercebiotech.com",
        "https://www.biopharmadive.com"
    ]

    full_report = ""

    for source in target_sources:
        print(f"🔍 Analyzing {source}...")
        try:
            # We ask for a simple summary of ONE site at a time
            # This uses fewer 'search' resources per request
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite-preview",
                config={'tools': [{'google_search': {}}]},
                contents=f"Find the top 2 biotech headlines from {source} from the last 24 hours."
            )
            full_report += f"\nFROM {source}:\n{response.text}\n"
            
            # ☕ The "Nap": Wait 10 seconds between sites to reset your quota
            time.sleep(10) 
            
        except Exception as e:
            print(f"⚠️ Skipped {source} due to limit: {e}")

    # Final Executive Polish
    if full_report:
        print("\n--- 🚀 FINAL EXECUTIVE SUMMARY ---")
        final_brief = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=f"Turn these notes into a professional 9:00 AM briefing: {full_report}"
        )
        print(final_brief.text)

if __name__ == "__main__":
    run_gentle_agent()
