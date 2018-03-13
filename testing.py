import requests
url = "http://www.politifact.com/api/statements/truth-o-meter/people/barack-obama/json/?n=6&callback=?"
response = requests.get(url)
#data = json.loads(response.read())
print response.json()
