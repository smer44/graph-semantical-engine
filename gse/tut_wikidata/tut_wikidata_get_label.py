from argparse import ArgumentParser

import requests


def search_entities(search_word):
    # Define the SPARQL query to search for entities by label
    query = f"""
    SELECT ?item ?itemLabel
    WHERE 
    {{
      ?item rdfs:label "{search_word}"@en .
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    """

    url = 'https://query.wikidata.org/sparql'
    headers = {
        'User-Agent': 'YourBot/0.1 (your.email@example.com) Python-requests/2.22',
        'Accept': 'application/sparql-results+json'
    }
    response = requests.get(url, headers=headers, params={'query': query})
    if response.status_code == 200:
        # Parse the response
        data = response.json()

        # Print the results
        for item in data['results']['bindings']:
            print(item['item']['value'], '-', item['itemLabel']['value'])
    else:
        print('Error:', response.status_code)


def cli():
    parser = ArgumentParser(
        prog='Search entity labels',
        description='The program to search entity label',
    )
    parser.add_argument(
        'search_word',
        nargs=1,
        type=str,
        help='Word to search',
    )
    args = parser.parse_args()
    search_entities(args.search_word[0])


if __name__ == '__main__':
    cli()
