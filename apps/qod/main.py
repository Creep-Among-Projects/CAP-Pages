import os

import requests


PEXELS_HEADERS = {
    'Authorization': os.getenv('PEXELS_API_KEY')
}

PEXELS_PARA = {
    'query': 'nature',
    'orientation': 'landscape'
}


# Fetch Pexels Images
print(requests.get('https://api.pexels.com/v1/search', headers=PEXELS_HEADERS, params=PEXELS_PARA))
