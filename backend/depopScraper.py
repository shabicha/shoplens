
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re
import apiKeys

#  Scrape.do token
SCRAPE_DO_TOKEN = apiKeys.token

print("✓ Scrape.do token loaded")

def get_depop_links(best_colour, best_brand, best_object):
    print("\n" + "=" * 60)
    print("STAGE 3A: Starting Depop scraping...")
    print("=" * 60)

    try:
        # Construct search URL
        if best_brand != "no brand":
            search_url = f"https://www.depop.com/search/?q={best_colour}+{best_brand}+{best_object}"
        else:
            search_url = f"https://www.depop.com/search/?q={best_colour}+{best_object}"

        print(f"✓ Search URL constructed: {search_url}")
        print("  → Sending request to Scrape.do API...")

        api_url = "https://api.scrape.do"
        params = {
            'token': SCRAPE_DO_TOKEN,
            'url': search_url,
            'render': 'true',
            'customHeaders': 'true'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        response = requests.get(api_url, params=params, headers=headers, timeout=60)
        print(f"✓ Response received: Status {response.status_code}")

        if response.status_code != 200:
            print(f"✗ ERROR: API returned status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        all_links = soup.find_all("a", href=True)
        print(f"✓ Found {len(all_links)} total anchor tags")

        uniqueListing = {}
        links = []
        products_found = 0

        for a in soup.find_all("a", href=True):
            if "/products/" in a["href"]:
                products_found += 1
                hrefClean = a['href'].strip('\\"')
                full_url = f"https://www.depop.com{hrefClean}"

                # Extract product name from href (remove /products/ and trailing /, replace - with space)
                product_name = hrefClean.replace("/products/", "").replace("/", "").replace("-", " ")
                product_name = " ".join(product_name.split()[1:])

                # Extract price
                product_card = a.find_next("div", class_="styles_productAttributes__nt3TO")
                price = None
                if product_card:
                    discounted = product_card.find("p", attrs={"aria-label": "Discounted price"})
                    full_price = product_card.find("p", attrs={"aria-label": "Full price"})
                    generic_price = product_card.find("p", attrs={"aria-label": "Price"})
                    if discounted:
                        price = discounted.get_text(strip=True)
                    elif full_price:
                        price = full_price.get_text(strip=True)
                    elif generic_price:
                        price = generic_price.get_text(strip=True)

                # Find main image
                img = a.find_all("img", src=True)
                for i in img:
                    class_attr = i.get("class")
                    if class_attr:
                        for c in class_attr:
                            if "_mainImage_e5j9l_11" in c or "mainImage" in c:
                                src = i.get("src", "")
                                uniqueID = re.search(r"/b1/(\d+)/", src)
                                if not uniqueID:
                                    uniqueID = re.search(r"/(\d{8,})", src)

                                if uniqueID:
                                    uniqueID = uniqueID.group(1)
                                    if uniqueID not in uniqueListing:
                                        uniqueListing[uniqueID] = 0
                                        srcClean = src.strip('\\"')
                                        links.append([full_url, srcClean, product_name, price])
                                        break

        print(f"\n✓ Processing complete")
        print(f"✓ Total products found: {products_found}")
        print(f"✓ Unique listings extracted: {len(links)}")

        if len(links) > 0:
            print("\n📦 First 3 results:")
            for i, (url, img, name, price) in enumerate(links[:3]):
                print(f"  {i+1}. {url}")
                print(f"     IMG: {img[:80]}...")
                print(f"     NAME: {name}")
                print(f"     PRICE: {price}")
        else:
            print("\n⚠ WARNING: No listings extracted!")

        return links

    except requests.exceptions.RequestException as e:
        print(f"\n✗ ERROR: Network/API error: {e}")
        return []
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []

print("✓ Depop scraper function defined\n")
