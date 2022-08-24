#################################################################
#
# summoning-51ckn355 - AI generated cards and sets for Cockatrice
# written by Benjamin Gleitzman (gleitz@mit.edu)
# Code: https://github.com/gleitz/summoning-51ckn355
# Discord Bot Changes by Alonso Astroza
#################################################################


import argparse
import json
import time
from urllib.parse import quote

import requests
from slugify import slugify
#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options


CARD_INFO_GENERATION_URL = 'https://backend-dot-valued-sight-253418.ew.r.appspot.com/api/v1/card'
CARD_ART_GENERATION_URL = 'https://backend-dot-valued-sight-253418.ew.r.appspot.com/api/v1/art'
CARD_DISPLAY_URL = 'https://adventuresofyou.online/urza'

def generate(name, mana_cost):
    card = _generate_card(name, mana_cost)
    card_art_url = _generate_card_art_url(card)
    card_name = card['name']

    card['url'] = f'https://corsproxy.io/?{quote(card_art_url)}'
    card['filename'] = f'{slugify(card_name)}_{int(time.time())}.png'

    #print("Finished card:")
    #print(json.dumps(card, indent=4))
    return _download_card(card)

def _generate_card(name, mana_cost):
    card = {
        "deck_name": "",
        "name": name or "",
        "manaCost": mana_cost or "",
        "types": "",
        "subtypes": "",
        "text": "",
        "power": "",
        "toughness": "",
        "flavorText": "",
        "rarity": "",
        "loyalty": "",
        "url": "",
        "basic_land": "",
        "cardId": ""
    }

    print("Inventing card")
    response = requests.request("GET",
                                CARD_INFO_GENERATION_URL,
                                params={"presets": json.dumps(card),
                                        "deckBuilder": "false",
                                        "temperature": "1"})
    return response.json()

def _generate_card_art_url(card):
    print("Fetching artwork")
    response = requests.request("GET",
                                CARD_ART_GENERATION_URL,
                                params={"card": json.dumps(card)})

    wombo_task_id = response.json()['wombo_task_id']
    time.sleep(10)

    state = "incomplete"
    while state != "completed":
        response = requests.request("GET",
                                    f'{CARD_ART_GENERATION_URL}/latest',
                                    params={"wombo_task_id": wombo_task_id})
        state = response.json()['state']
        if state != "completed":
            print("Still waiting...")
            time.sleep(5)

    return response.json()['art_url']

def _download_card(card):
    #driver = _get_driver()

    url = f'{CARD_DISPLAY_URL}?encoded=1&card={quote(json.dumps(card))}'
    print("Printing card...")
    #print(url)
    return url