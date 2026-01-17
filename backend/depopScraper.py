
import requests
from pprint import pprint
from bs4 import BeautifulSoup
import re

#  Scrape.do token
SCRAPE_DO_TOKEN = "6724282cfca649fabb5a54049ab12fd21d884af297e" 

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
        
        # Scrape.do API endpoint
        api_url = "https://api.scrape.do"
        
        params = {
            'token': SCRAPE_DO_TOKEN,
            'url': search_url,
            'render': 'true',  # Enable JavaScript rendering
            'customHeaders': 'true'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Get response from Scrape.do
        response = requests.get(api_url, params=params, headers=headers, timeout=60)
        
        print(f"✓ Response received: Status {response.status_code}")
        print(f"✓ Response size: {len(response.text)} characters")
        
        # Check for errors
        if response.status_code != 200:
            print(f"✗ ERROR: API returned status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return []
        
        # Save HTML for debugging
        #html_filename = 'depop_scrapedo_response.html'
        #with open(html_filename, 'w', encoding='utf-8') as f:
        #    f.write(response.text)
        #print(f"✓ HTML saved to {html_filename}")
        
        # Parse links to product listings & corresponding images
        print("  → Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(response.text, "html.parser")
        print("✓ HTML parsed")
        
        # Find all anchor tags
        all_links = soup.find_all("a", href=True)
        print(f"✓ Found {len(all_links)} total anchor tags")
        
        # Find all anchor tags with product URLs
        uniqueListing = {}
        links = []
        products_found = 0
        
        print("  → Processing product links...")
        for a in soup.find_all("a", href=True):
            if "/products/" in a["href"]:
                products_found += 1
                hrefClean = a['href'].strip('\\"')
                full_url = f"https://www.depop.com{hrefClean}"
                
                # Find the image inside <a> tag
                img = a.find_all("img", src=True)
                
                if products_found <= 3:
                    print(f"    Product {products_found}: {len(img)} images found")
                
                for i in img:
                    class_attr = i.get("class")
                    if class_attr:
                        # Find image within mainImage class
                        for c in class_attr:
                            if "_mainImage_e5j9l_11" in c or "mainImage" in c:
                                src = i.get("src", "")
                                uniqueID = re.search(r"/b1/(\d+)/", src)
                                
                                if not uniqueID:
                                    uniqueID = re.search(r"/(\d{8,})", src)
                                
                                # No duplicates
                                if uniqueID:
                                    uniqueID = uniqueID.group(1)
                                    if uniqueID not in uniqueListing:
                                        uniqueListing[uniqueID] = 0
                                        srcClean = src.strip('\\"')
                                        links.append([full_url, srcClean])
                                        
                                        if len(links) <= 3:
                                            print(f"      ✓ Added listing {len(links)}")
                                            print(f"        URL: {full_url[:60]}...")
                                            print(f"        IMG: {srcClean[:60]}...")
                                break
        
        print(f"\n✓ Processing complete")
        print(f"✓ Total products found: {products_found}")
        print(f"✓ Unique listings extracted: {len(links)}")
        
        if len(links) > 0:
            print("\n📦 First 3 results:")
            for i, (url, img) in enumerate(links[:3]):
                print(f"  {i+1}. {url}")
                print(f"     {img[:80]}...")
        else:
            print("\n⚠ WARNING: No listings extracted!")
            print("  → Check your Scrape.do token")
            print("  → Check if you have credits remaining")
            print("  → Check the saved HTML file for debugging")
        
        print(f"\nReturning {len(links)} links")
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