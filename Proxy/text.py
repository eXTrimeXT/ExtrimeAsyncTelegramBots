import requests

proxies = {
  'http': 'http://52.143.130.19:3128',
}

r = requests.get('http://example.org', proxies={"http": "http://52.143.130.19:3128"}).json
print(r)
