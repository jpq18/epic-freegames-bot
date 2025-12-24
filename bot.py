import os, json, requests
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.environ["8230617052:AAGvh5aIFsc6nL8kA07_lIa9AqeqaZc1okM"]
CHANNEL_ID = os.environ["@iraqfreegames"]
STATE_FILE = "posted.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_state(ids):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f)

def fetch_free_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
    data = requests.get(url).json()
    items = data["data"]["Catalog"]["searchStore"]["elements"]
    games = []

    for it in items:
        promos = it.get("promotions")
        if not promos:
            continue

        offers = promos.get("promotionalOffers")
        if not offers:
            continue

        offer = offers[0]["promotionalOffers"][0]
        if offer["discountSetting"]["discountPercentage"] != 0:
            continue

        slug = it.get("productSlug") or it.get("urlSlug")
        img = it.get("keyImages", [{}])[0].get("url")

        games.append({
            "id": it["id"],
            "title": it["title"],
            "url": f"https://store.epicgames.com/p/{slug}",
            "image": img,
            "end": offer["endDate"]
        })
    return games

def post(bot, g):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 صفحة اللعبة", url=g["url"])]
    ])
    text = f"🔥 لعبة مجانية الآن!\n\n🎯 {g['title']}\n⏳ ينتهي: {g['end']}"
    bot.send_photo(CHANNEL_ID, g["image"], caption=text, reply_markup=kb)

def main():
    bot = Bot(8230617052:AAGvh5aIFsc6nL8kA07_lIa9AqeqaZc1okM)
    posted = load_state()

    for g in fetch_free_games():
        if g["id"] in posted:
            continue
        post(bot, g)
        posted.add(g["id"])

    save_state(posted)

if __name__ == "__main__":
    main()
