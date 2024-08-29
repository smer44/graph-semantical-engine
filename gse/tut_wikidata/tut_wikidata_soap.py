from argparse import ArgumentParser

import requests


def request_entity(entity_id):
    url = f'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'ids': entity_id,
        'format': 'json'
    }
    headers = {
        'User-Agent': 'YourBot/0.1 (your.email@example.com) Python-requests/2.22'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        # Parse the response, returns more data then sparql
        data = response.json()

        # Get the entity data
        entity_data = data['entities'][entity_id]

        # Extract the claims (statements)
        claims = entity_data['claims']

        # Get the superclasses (P279 - subclass of)
        if 'P279' in claims:
            for superclass in claims['P279']:
                superclass_id = superclass['mainsnak']['datavalue']['value']['id']

                # Fetch the label for the superclass
                superclass_url = f'https://www.wikidata.org/wiki/Special:EntityData/{superclass_id}.json'
                superclass_response = requests.get(superclass_url, headers=headers)

                if superclass_response.status_code == 200:
                    superclass_data = superclass_response.json()
                    superclass_label = superclass_data['entities'][superclass_id]['labels']['en']['value']
                    print(f'{superclass_id} - {superclass_label}')
    else:
        print('Error:', response.status_code)


def cli():
    parser = ArgumentParser(
        prog='SOAP entity getter',
        description='The program to get entity throw SOAP',
    )
    parser.add_argument(
        'object_id',
        nargs=1,
        type=str,
        help='Object\'s ID',
    )
    args = parser.parse_args()
    request_entity(args.object_id[0])


if __name__ == '__main__':
    cli()
