import requests

# Define the word to search for
search_word = "cat"

# Define the SPARQL query to search for entities by label
query = f"""
SELECT ?item ?itemLabel
WHERE 
{{
  ?item rdfs:label "{search_word}"@en .
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
"""

# Define the endpoint URL
url = 'https://query.wikidata.org/sparql'

# Set the headers
headers = {
    'User-Agent': 'YourBot/0.1 (your.email@example.com) Python-requests/2.22',
    'Accept': 'application/sparql-results+json'
}

# Make the request
response = requests.get(url, headers=headers, params={'query': query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the response
    data = response.json()

    # Print the results
    for item in data['results']['bindings']:
        print(item['item']['value'], '-', item['itemLabel']['value'])
else:
    print('Error:', response.status_code)

# Example Output
# http://www.wikidata.org/entity/Q146 - cat
# ...
