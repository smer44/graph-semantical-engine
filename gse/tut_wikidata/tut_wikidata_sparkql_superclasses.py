from argparse import ArgumentParser

import requests


def dfs_once(item, cfn):
    stack = [item]
    dejavu = set()
    while stack:
        item = stack.pop()
        for child in cfn(item):
            if child not in dejavu:
                dejavu.add(child)
                stack.append(child)


def handle_object(obj):
    object_id, object_name = obj
    # Define the SPARQL query for direct superclasses
    # Q146 (cats) and P279 (subclass of) predicate
    query = f"""
    SELECT ?superclass ?superclassLabel
    WHERE 
    {{
      wd:{object_id} wdt:P279 ?superclass .  
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
            child_id = item["superclass"]["value"].split("/")[-1]
            child_name = item['superclassLabel']['value']
            print(object_name, " subclass_of ",child_name)
            #print(child, item['superclass']['value'], '-', item['superclassLabel']['value'])
            yield child_id, child_name
            #print(item)

    else:
        print('Error:', response.status_code)


def cli():
    parser = ArgumentParser(
        prog='SPARKQL entity searcher',
        description='The program to search superclass by SPARKQL',
    )
    parser.add_argument(
        'entity_id',
        nargs=1,
        type=str,
        help='Entity\'s ID',
    )
    parser.add_argument(
        'entity_name',
        nargs=1,
        type=str,
        help='Entity\'s name',
    )
    args = parser.parse_args()
    dfs_once(
        (args.entity_id[0], args.entity_name[0]),
        handle_object,
    )


if __name__ == '__main__':
    cli()
