import time
import requests
import feedparser
import os

# Webhook URL közvetlenül beállítva
WEBHOOK_URL = "https://discord.com/api/webhooks/1520846598698045490/OukWGlhNqy-w575bqJpw3sYAoHHXrfSK9HcMjmHSCsTWo5KV5nz2HGpAzZcN3mKe6yIA"

PROFILES = [
    "tobimono2", "United24media", "InformNapalm", "EsGeeks", "sentdefender", 
    "threatcluster", "FoxNews", "ChristinaManic", "FairfaxGOP", "NewYorker", 
    "cnnbrk", "BBCBreaking", "ABC", "News_Ejazah", "CBSNews", "bellingcat", 
    "Osinttechnical", "OsintTV", "OsintUpdates", "AggregateOsint", 
    "realDonaldTrump", "TheHackersNews", "newsycombinator", "cyber", 
    "DNewsHungary", "Crypto_Newslett", "cryptonwsuk", "thenexus_team"
]

INSTANCE = "https://nitter.poast.org"

# Itt tároljuk a legutóbbi poszt címét, hogy ne spamoljon
last_post_titles = {}

def send_to_discord(title, link):
    payload = {"content": f"📢 **Új bejegyzés:** {title}\n{link}"}
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Discord küldési hiba: {e}")

def main():
    print("🚀 Nitter RSS Crawler elindult...")
    
    while True:
        for profile in PROFILES:
            rss_url = f"{INSTANCE}/{profile}/rss"
            try:
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    latest = feed.entries[0]
                    title = latest.title
                    link = latest.link
                    
                    # Ha a poszt címe új, elküldjük
                    if profile not in last_post_titles:
                        last_post_titles[profile] = title
                    elif last_post_titles[profile] != title:
                        print(f"Új poszt találva: {profile}")
                        send_to_discord(title, link)
                        last_post_titles[profile] = title
            except Exception as e:
                print(f"Hiba a {profile} RSS olvasásakor: {e}")
            
            # Rövid szünet a profilok között
            time.sleep(2)
        
        # 300 másodperces várakozás a következő kör előtt
        print("Ciklus kész, várakozás 300 mp...")
        time.sleep(300)

if __name__ == "__main__":
    main()
