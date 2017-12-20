import json
import pprint
import requests
from itertools import chain


with open('europeanaApiKey.txt', mode='r', encoding='utf-8') as key:
    europeana_apikey = key.read()


def europeana_search_query(search_query, api_key, query_refinement_list=None, rows=100, profile='standard', cursor=None):
    """Collects up to 100 items from a europeana search matching given search paramaters, using europeana Search API.
    query_refinement_list can get any number of strings
    Returns json object as a dictionary."""
    url = 'https://www.europeana.eu/api/v2/search.json'
    payload = {'query': search_query, 'wskey': api_key, 'rows': rows}
    if query_refinement_list is not None:
        payload['qf'] = query_refinement_list
    if profile != 'standard':
        payload['profile'] = profile
    if cursor is not None:
        payload['cursor'] = cursor
    search = requests.get(url, params=payload)
    return search.json()


def europeana_all_items(search_query, api_key, query_refinement_list=None, profile='standard'):
    """Returns list of all items in a europeana search query using cursor based pagination.
    Returns iterator object"""
    search_results = []
    cursor = '*'
    while cursor is not None:
        search = europeana_search_query(search_query, api_key, query_refinement_list=query_refinement_list, profile=profile, cursor=cursor)
        search_results = chain(search_results, search.get('items'))
        cursor = search.get('nextCursor')
    return search_results


def hit_count(query, item_list):
    """Returns number of query hits in item for items in item_list"""
    hits = []
    for n, item in enumerate(item_list):
        hit = json.dumps(item).lower().count(query.lower())
        hits.append((n, hit))
    return hits


def key_value_finder(desired_key, query_string, dic):
    """Returns True if dict has key and if key has query_string in value"""
    if desired_key in dic:
        desired_key_value = dic.get(desired_key)
        if type(desired_key_value) == str:
            return query_string.lower() in desired_key_value.lower()
        else:
            return query_string.lower() in json.dumps(desired_key_value).lower()
    else:
        return False


def key_value_finder_agg(list_of_keys, desired_string, list_of_dicts):
    """Returns list with tuples that look like this (index_of_item_in_lod, number_of_successful_finds_in_item)"""
    hits = []
    for n, dict in enumerate(list_of_dicts):
        count = 0
        for desired_key in list_of_keys:
            if key_value_finder(desired_key, desired_string, dict):
                count += 1
        hits.append((n, count))
    return hits


search = ('"Mona Lisa"', europeana_apikey)
#TYPE is case sensitive, possible values are IMAGE, TEXT, SOUND, VIDEO, 3D. If blank it returns all types.

data1 = europeana_search_query(*search, query_refinement_list=['TYPE:IMAGE'])
data2 = europeana_search_query(*search, query_refinement_list=['TYPE:IMAGE'], profile='rich')
data3 = europeana_search_query(*search, query_refinement_list=['TYPE:IMAGE'], profile='minimal')


item_list1 = data1.get('items')
item_list2 = data2.get('items')
item_list3 = data3.get('items')

print(len(item_list1), len(item_list2), len(item_list3))

for n, item in enumerate(zip(item_list1, item_list2, item_list3)):
    print(n, item[0].get('title'), item[0].get('score'), item[1].get('title'), item[1].get('score'), item[2].get('title'), item[2].get('score'))

data = list(europeana_all_items(*search, profile='rich', query_refinement_list=['TYPE:IMAGE']))
chosen_keys = ['title', 'dcDescription']
desired_string = 'Mona Lisa'

pprint.pprint(key_value_finder_agg(chosen_keys, desired_string, data))
pprint.pprint(hit_count(desired_string, data))

