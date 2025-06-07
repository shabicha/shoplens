import requests
from pprint import pprint
import apiKeys
import CLIPFeatureIdentify
from bs4 import BeautifulSoup
import re

def get_depop_links(best_colour, best_brand, best_object):

  if best_brand !="no brand":
    payload = {
        'source': 'universal',
        'url': f"https://www.depop.com/search/?q={best_colour}+{best_brand}+{best_object}",
        "render": "html"
    }
  else:
    payload = {
        'source': 'universal',
        'url': f"https://www.depop.com/search/?q={best_colour}+{best_object}",
        "render": "html"
    }

  # Get response.
  response = requests.request(
      'POST',
      'https://realtime.oxylabs.io/v1/queries',
      auth=(apiKeys.user, apiKeys.pass1),
      json=payload,
  )

  # Instead of response with job status and results url, this will return the
  # JSON response with the result.

  #parse links to product listings & corrosponding 960w image

  soup = BeautifulSoup(response.text, "html.parser")

  # Find all anchor tags with product URLs
  uniqueListing = {}

  links = []
  for a in soup.find_all("a", href=True):
      if "/products/" in a["href"]:
          hrefClean = a['href'].strip('\\"')

          full_url = f"https://www.depop.com{hrefClean}"
          

          # find the image inside <a> tag
          img = a.find_all("img", src=True)
          for i in img:
            class_attr = i.get("class")
            if class_attr:
              #find image within mainImage_e5j9l_11 class
              for c in class_attr:
                if "_mainImage_e5j9l_11" in c:
                  uniqueID = re.search(r"/b1/(\d+)/", i["src"])
                  #no duplicates
                  if uniqueID:
                    uniqueID = uniqueID.group(1)
                  if uniqueID not in uniqueListing:
                    uniqueListing[uniqueID] = 0
                    srcClean = i["src"].strip('\\"')
                    
                    links.append([full_url, srcClean])
  
  print(links)
  return links
