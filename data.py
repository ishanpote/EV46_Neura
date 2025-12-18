import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re

def scrape_stealth(search_query, max_pages=2):
    product_list = []
    
    # This header makes you look like a real Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }

    for page in range(1, max_pages + 1):
        print(f"Attempting Page {page}...")
        # Using the 'rt=nc' and '_ipg' parameters to look like a standard browser filter
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query.replace(' ', '+')}&_pgn={page}&rt=nc&_ipg=60"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Blocked with status code: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Updated selector for 2025 eBay layout
            items = soup.find_all('div', {'class': 's-item__info'})

            for item in items:
                title_el = item.find('div', {'class': 's-item__title'})
                price_el = item.find('span', {'class': 's-item__price'})
                
                if title_el and price_el:
                    title = title_el.text.strip()
                    if "Shop on eBay" in title or "Announcement" in title: continue
                    
                    price_text = price_el.text.strip()
                    
                    # Extract location (The 'Red Flag' for Grey Markets)
                    loc_el = item.select_one('.s-item__location, .s-item__itemLocation')
                    location = loc_el.text.replace("from ", "").strip() if loc_el else "USA/Domestic"

                    product_list.append({
                        "Title": title,
                        "Price_Raw": price_text,
                        "Seller_Location": location
                    })
            
            print(f"Successfully found {len(product_list)} items so far...")
            time.sleep(random.uniform(3, 7)) # Be very polite
            
        except Exception as e:
            print(f"Request failed: {e}")
            break

    return pd.DataFrame(product_list)

# --- EXECUTION ---
# Try a very common item that has high volume
df = scrape_stealth("Samsung Galaxy S24 Ultra", max_pages=2)

if not df.empty:
    # Clean the price: handle "$1,200.00" or "$900 to $1,100"
    def clean_price(price_str):
        numbers = re.findall(r"[\d.]+", price_str.replace(',', ''))
        return float(numbers[0]) if numbers else 0.0

    df['Price_Clean'] = df['Price_Raw'].apply(clean_price)
    df = df[df['Price_Clean'] > 0] # Remove items with no price
    
    df.to_csv("grey_market_data.csv", index=False)
    print("\n--- DONE ---")
    print(f"Saved {len(df)} rows to grey_market_data.csv")
    print(df[['Title', 'Price_Clean', 'Seller_Location']].head())
else:
    print("Still no data. If you are on Google Colab, eBay might be blocking the Colab IP. Try running this locally on your laptop.")