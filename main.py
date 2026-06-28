import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Discord Webhook
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1520846598698045490/OukWGlhNqy-w575bqJpw3sYAoHHXrfSK9HcMjmHSCsTWo5KV5nz2HGpAzZcN3mKe6yIA"

# Nitter profilok listája
NITTER_PROFILES = [
    "https://nitter.net/tobimono2", "https://nitter.net/United24media", "https://nitter.net/InformNapalm",
    "https://nitter.net/EsGeeks", "https://nitter.net/sentdefender", "https://nitter.net/threatcluster",
    "https://nitter.net/FoxNews", "https://nitter.net/ChristinaManic", "https://nitter.net/FairfaxGOP",
    "https://nitter.net/NewYorker", "https://nitter.net/cnnbrk", "https://nitter.net/BBCBreaking",
    "https://nitter.net/ABC", "https://nitter.net/News_Ejazah", "https://nitter.net/CBSNews",
    "https://nitter.net/bellingcat", "https://nitter.net/Osinttechnical", "https://nitter.net/OsintTV",
    "https://nitter.net/OsintUpdates", "https://nitter.net/AggregateOsint", "https://nitter.net/realDonaldTrump",
    "https://nitter.net/TheHackersNews", "https://nitter.net/newsycombinator", "https://nitter.net/cyber",
    "https://nitter.net/DNewsHungary", "https://nitter.net/Crypto_Newslett", "https://nitter.net/cryptonwsuk",
    "https://nitter.net/thenexus_team"
]

def kuld_discordra(embed):
    payload = {"username": "Velox Nitter Crawler", "embeds": [embed]}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Discord hiba: {e}")

def scrap_nitter(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # A legfrissebb tweet keresése (Nitter specifikus osztályok)
        tweet = soup.find("div", class_="timeline-item")
        if not tweet: return None
        
        tweet_id = tweet.get("data-permalink-path")
        content = tweet.find("div", class_="tweet-content").get_text()
        user = tweet.find("a", class_="fullname").get_text()
        
        # Média keresése
        img_tag = tweet.find("div", class_="attachment image")
        img_url = img_tag.find("img")["src"] if img_tag else None
        
        return {
            "id": tweet_id,
            "text": content,
            "user": user,
            "image": f"https://nitter.net{img_url}" if img_url and img_url.startswith("/") else img_url,
            "url": f"https://nitter.net{tweet_id}"
        }
    except Exception:
        return None

def main():
    mar_ellenorzott = {} # {url: tweet_id}
    print("🚀 Nitter Crawler elindult")
    
    while True:
        for profile in NITTER_PROFILES:
            data = scrap_nitter(profile)
            if data and data["id"] != mar_ellenorzott.get(profile):
                print(f"Új bejegyzés: {data['url']}")
                
                embed = {
                    "title": f"Új tweet: {data['user']}",
                    "description": data["text"],
                    "url": data["url"],
                    "color": 3447003
                }
                if data["image"]:
                    embed["image"] = {"url": data["image"]}
                
                kuld_discordra(embed)
                mar_ellenorzott[profile] = data["id"]
            
            time.sleep(10) # Ne kapjunk ban-t a Nittertől
        time.sleep(300)

if __name__ == "__main__":
    main()
