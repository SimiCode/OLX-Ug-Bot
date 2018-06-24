#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""This is a simple olx bot. It picks its params (email, search query) from a web form which users fill and
   then searches olx uganda for that item hourly. If a new result is found, The bot should email the url
   of the product to the subscribed user
"""

# import re
import json
import requests
# from bs4 import BeautifulSoup

import sys
sys.path.insert(0, '/home/bots/')
import simi

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


__author__ = "J Edison Abahurire"
__credits__ = ["J Edison Abahurire", "Al Sweigart", ]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = "abahedison1@outlook.com"
__status__ = "Production"


def main():
    '''this is the function that takes in a bot_tasks dic, a stored_ids dic and searches for
    the quesries from the tasks dic (values) while comparing their ids to ids that were
    seen in results and stored. If product id is new, email is sent to subscriber (key)
    and id is stored in stored_ids
    '''

    # UNQUOTE THIS
    # WORKS! https://www.olx.co.ug/api/items?query={%22filters%22:{},%22text%22:%22kindle%22,%22sorting%22:%22desc-creation%22}

    for email, search_term in bot_tasks.items():

        search_url = "https://www.olx.co.ug/api/items?query={%22filters%22:{},%22text%22:%22"+ "%20".join(search_term.strip().split()) +"%22,%22sorting%22:%22desc-creation%22}"
        # sample: "https://www.olx.co.ug/api/items?query={%22filters%22:{},%22text%22:%22kindle%22,%22sorting%22:%22desc-creation%22}"
        print(search_url)

        headers = {
             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
             'accept-encoding': 'gzip, deflate, br',
             'accept-language': 'en-US,en;q=0.9',
             'authority': 'www.olx.co.ug',
             'cache-control': 'max-age=0',
             'cookie': 'optimizelyId=66115288-9390-41bc-a380-089f9c4cc7d7; ldTd=true; onap=163a9f747f2x1bb1e62e-4-163e23c3ef4x5a284a05-12-1528510815; 30067a00309fd87576a1bc675141543e=52e0d967addf08eed11644c4d96c2737',
             'dnt': '1',
             'if-none-match': 'W/"7f29b2d7da6e4ac830477a717d8a7dbf"',
             'method': 'GET',
             'path': '/api/items?query={%22filters%22:{},%22text%22:%22kindle%22,%22sorting%22:%22desc-creation%22}',
             'scheme': 'https',
             'upgrade-insecure-requests': '1',
             'user-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'
        }

        response_json = json.loads(requests.get(search_url, headers=headers).text)

        results = response_json['data']
        print(len(results), ' = len of results', '\n')
        # print(elements)

        for item in results:
            item_id = item['id']

            if not item_id in stored_ids:

                title = item['title']
                product_url = 'https://www.olx.co.ug/item/' + "-".join(title.lower().split()) + '-iid-' + item_id
                print(product_url)
                # send email
                send_mail(email, search_term, product_url)
                # store product id
                stored_ids.append(item_id)
            else:
                print('Product already scraped')

    # add new ids to history list after all searches have been made
    simi.xdump( '/home/bots/olx_history.txt', list(set(stored_ids)) )



def send_mail(subscriber_email, search_term, product_url):

    msg = MIMEMultipart()
    body = 'Your serach a new product up for sale here : '+ product_url +' \n\nYours, Bot'

    msg['From'] = "sales@botsmart.uk"
    msg['To'] = subscriber_email
    msg['Subject'] = "OLX - " + search_term

    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(msg['From'], "G0d15G00d")
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()


if __name__ == '__main__':

    # simi.xdump( 'olx_history.txt', [] )
    # simi.xdump('olx_tasks.pickle', {'abahedison1@outlook.com':'kindle'})

    # tasks tbd
    bot_tasks = simi.xload('/home/bots/subscriptions.olx')
    # bot_tasks = {}

    # store of products already indexed
    stored_ids = simi.xload('/home/bots/olx_history.txt')

    main()






