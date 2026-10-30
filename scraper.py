#!/usr/bin/env python3

'''
A high-level scraper to find ea. season's Formula One Champion
'''

import csv, html, re, requests, sys, time
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

INDEX_URL = 'https://en.wikipedia.org/wiki/List_of_Formula_One_seasons'
WIKIPEDIA_URL = 'https://en.wikipedia.org'
HEADERS = {'User-Agent': 'f1-scraper/1.0'}

# Functions

def usage(status: int=0) -> None:
    print(f'''Usage: scraper [-n WORKERS] [OUTPUT]
    -n WORKERS Number of threads to use, which defaults to 8

    If OUTPUT is not provided, then it defaults to f1_champions.csv.''', file=sys.stderr)
    sys.exit(status)

def fetch(url: str) -> str:
    ''' Return the HTML of the url.'''
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text

def clean(text: str) -> str:
    '''
    >>> clean('<a href="/wiki/Lando_Norris">Lando&#160;Norris</a><sup>[1]</sup>')
    'Lando Norris'
    '''
    text = re.sub('<[^>]*>', '', text)
    text = re.sub(r'\[[^\]]*\]', '', text)
    return ' '.join(html.unescape(text).split())

def season_urls(text: str) -> dict[int, str]:
    '''
    >>> season_urls('<a href="/wiki/1950_Formula_One_season#Results">1950</a>')
    {1950: 'https://en.wikipedia.org/wiki/1950_Formula_One_season'}
    '''
    
    # Pulls from the index page
    links = re.findall(r'href="(?:https://en\.wikipedia\.org)?(/wiki/(\d{4})_Formula_One_(?:season|World_Championship))[#"]', text)
    return dict(sorted((int(year), WIKIPEDIA_URL + path) for path, year in links))

# Funtional Programming also with a generator instead of a loop

def champion(text: str, prefix: str) -> str:
    '''
    >>> champion("<a>Drivers' Champion</a>: <a>Lando Norris</a><br/>", 'Drivers')
    'Lando Norris'
    '''
    match = re.search(prefix + r"[^<]*Champion(?:</a>)?:(.*?)(?:<br|</td|</span)", text, re.DOTALL)
    return clean(match.group(1)) if match else ''    

    #cells= re.findall(r'<t[hd](?:\s[^>]*)?>(.*?)</t[hd]>', text, re.DOTALL)
    #return next((clean(value) for label, value in zip(cells, cells[1:]) if clean(label).startswith(prefix)), '')

def scrape_season(year: int, url: str) -> dict:
    text = fetch(url)
    return {'season': year, 'driver': champion(text, 'Drivers'), 'constructor': champion(text, 'Constructors')}

# Main

def main(arguments: list[str]=sys.argv[1:]) -> None:
    workers = 8
    output = 'f1_champions.csv'

    # I used the course framework here heavily
    while arguments and arguments[0].startswith('-'):
        argument = arguments.pop(0)
        if argument == '-n':
            workers = int(arguments.pop(0))
        elif argument == '-h':
            usage(0)
        else:
            usage(1)

    if arguments:
        output = arguments.pop(0)

    start = time.time()
    urls = season_urls(fetch(INDEX_URL))

    # Concurrent.futures: pool of threads runs the scrape_season
    with ThreadPoolExecutor(max_workers=workers) as executor:
        seasons = list(executor.map(scrape_season, urls.keys(), urls.values()))

    elapsed = time.time() - start

    with open(output, 'w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['season', 'driver', 'constructor'])
        writer.writeheader()
        writer.writerows(seasons)

    titles = Counter(season['driver'] for season in seasons if season['driver']).most_common(3)

    print(f'Seasons: {len(seasons)} in {elapsed:.2f}s with {workers} workers(s) -> {output}')
    print(f'Titles: ' + ', '.join(f'{name} ({count})' for name, count in titles))

if __name__ == '__main__':
    main()

