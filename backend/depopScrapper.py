import requests
from pprint import pprint
import apiKeys

# Structure payload.
payload = {
    'source': 'universal',
    'url': 'https://www.depop.com/category/womens/bottoms/?categorypath=womens&categorypath=bottoms'
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('apiKeys.user', 'apiKeys.pass1'),
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with the result.
pprint(response.json())