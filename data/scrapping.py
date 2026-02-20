import requests
import pandas as pd
import time
import random
import os

BASE_URL = "https://www.vivino.com/api/explore/explore"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

WINE_TYPES = {
    1: "Red",
    2: "White",
    3: "Sparkling",
    4: "Rose",
    7: "Dessert",
    24: "Fortified"
}

RATING_BLOCKS = [
    (4.5, 5.0),
    (4.0, 4.5),
    (3.5, 4.0),
    (3.0, 3.5),
    (2.5, 3.0),
    (1.0, 2.5)
]

SAVE_EVERY_PAGES = 40

RAW_DIR = "raw"
os.makedirs(RAW_DIR, exist_ok=True)

RESUME_CSV = os.path.join(RAW_DIR, "vivino_all_types.csv")


# ---------------- SAFE REQUEST ----------------

def safe_request(payload, retries=3):
    for attempt in range(retries):
        r = requests.get(BASE_URL, params=payload, headers=HEADERS)

        if r.status_code == 200:
            return r

        if r.status_code == 429:
            print("Rate limit hit. Sleeping 90 seconds...")
            time.sleep(90)
            continue

        print(f"Attempt {attempt+1} failed ({r.status_code})")
        time.sleep(5)

    raise Exception("Failed after retries")


# ---------------- EXTRACTION ----------------

def extract_data(match, wine_type_label):
    # 🔹 Datos básicos
    vintage = match.get("vintage") or {}
    wine = vintage.get("wine") or {}
    region = wine.get("region") or {}
    country = region.get("country") or {}
    winery = wine.get("winery") or {}
    statistics = vintage.get("statistics") or {}
    prices = match.get("prices") or []

    # Precio
    price = None
    if isinstance(prices, list) and len(prices) > 0:
        price = prices[0].get("amount")

    # 🔹 Estilo
    style = wine.get("style") or {}
    baseline = style.get("baseline_structure") or {}

    return {
        # Identificación
        "wine_id": wine.get("id"),
        "wine_name": f"{wine.get('name') or ''} {vintage.get('year') or ''}".strip(),
        "winery": winery.get("name"),
        "year": vintage.get("year"),
        "wine_type": wine_type_label,

        # Ratings
        "rating": statistics.get("ratings_average"),
        "num_reviews": statistics.get("ratings_count"),

        # Precio
        "price": price,

        # Geografía
        "country": country.get("name"),
        "region": region.get("name"),

        # Estilo
        "style": style.get("name"),
        "style_body": style.get("body"),
        "style_acidity": style.get("acidity"),
        "intensity": baseline.get("intensity"),
        "sweetness": baseline.get("sweetness"),
        "tannin": baseline.get("tannin"),

        # 🔹 NOTA: sacamos grapes
        # "grapes": grapes_str
    }


# ---------------- SCRAPER ----------------

def scrape():

    existing_ids = set()

    # Cargar ids ya scrapeados si existe archivo
    if os.path.exists(RESUME_CSV):
        df_existing = pd.read_csv(RESUME_CSV)
        existing_ids = set(df_existing["wine_id"])
        print(f"Resuming. Already have {len(existing_ids)} wines.")

    for type_id, type_label in WINE_TYPES.items():

        print(f"\n===== Scraping {type_label} =====")

        for min_rating, max_rating in RATING_BLOCKS:

            print(f"Rating block: {min_rating} - {max_rating}")

            page = 1
            page_counter = 0
            consecutive_empty_pages = 0

            while True:

                payload = {
                    "country_codes[]": ["es"],
                    "currency_code": "EUR",
                    "min_rating": str(min_rating),
                    "max_rating": str(max_rating),
                    "order_by": "ratings_count",
                    "order": "asc",
                    "page": page,
                    "price_range_max": "500",
                    "price_range_min": "0",
                    "wine_type_ids[]": str(type_id),
                }

                print(f"{type_label} | Rating {min_rating}-{max_rating} | Page {page}")

                r = safe_request(payload)
                data = r.json()
                matches = data.get("explore_vintage", {}).get("matches", [])

                if not matches:
                    print("No more matches in this rating block.")
                    break

                rows = []

                for match in matches:
                    wine_data = extract_data(match, type_label)

                    if wine_data["wine_id"] in existing_ids:
                        continue

                    existing_ids.add(wine_data["wine_id"])
                    rows.append(wine_data)

                if rows:
                    temp_df = pd.DataFrame(rows)

                    temp_df.to_csv(
                        RESUME_CSV,
                        mode="a",
                        header=not os.path.exists(RESUME_CSV),
                        index=False
                    )

                    consecutive_empty_pages = 0  # reset if new wines found

                else:
                    consecutive_empty_pages += 1
                    print(f"No new wines added (streak: {consecutive_empty_pages})")

                if consecutive_empty_pages >= 3:
                    print("Stopping this rating block (no new wines).")
                    break

                page += 1
                page_counter += 1

                time.sleep(random.uniform(2.0, 4.0))


        print(f"Finished {type_label}")

    print("\nScraping completed.")


if __name__ == "__main__":
    scrape()