# Crawling using JIKAN API

import requests
import time
import json
import re
from datetime import datetime
import logging


with open('seeds/anime_url_test.json', 'r') as json_file:
    url_list = json.load(json_file)

dataFull = []

timeFileName = "{}_{}".format(datetime.today().strftime('%Y-%m-%d'), time.time())

logging.basicConfig(filename="log/log_{}.log".format(timeFileName), level=logging.INFO)

id_pattern = re.compile(r'/anime/(\d+)/')
for url in url_list:
    try:
        match = id_pattern.search(url)
        if match:
            anime_id = match.group(1)  # Extract the ID part

        jikanUrl = "https://api.jikan.moe/v4/anime/{}/full".format(anime_id)

        logging.info("Fetching data {}".format(url))
        animeData = requests.get(url = jikanUrl)

        if animeData.status_code == 200:
            logging.info("Successfully Fetching Data")
            logging.info("Request Status : {}".format(animeData.status_code))
        else:
            logging.error("Failed Fetching Data!")
            logging.error("Request Status : {}".format(animeData.status_code))

        data = animeData.json()

        dataFull.append(data['data'])

        time.sleep(2)
    except Exception as error:
        logging.error(error)
        continue

with open('result/anime_data_{}.json'.format(timeFileName), 'w') as json_file:
    try:
        logging.info("Dumping Data...")
        json.dump(dataFull, json_file, indent=4)
        logging.info("Successfully Dumping Data")
    except Exception as error:
        logging.error("Failed Dumping Data")
        logging.errot(error)