import os
import json
import datetime
import pytest
import requests
import logging
import hashlib
import math
import numpy
from io import StringIO

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_api_credentials
root_file_directory = os.path.dirname(os.path.realpath(__file__))
json_characters_template_file_path = os.path.join(os.path.dirname(root_file_directory),
                                              "common", "json_templates", "characters_template.json")

with open(json_characters_template_file_path) as f:
    json_characters_template_file = json.load(f)

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(level=logging.INFO)

PRIVATE_KEY = '6ec8f2171591da71c90dfba20fa3300a5ce9d2f6'
PUBLIC_KEY = '5cad12f837c7b8615de38a6c18e0f070'
PAGE_SIZE = 1

#PUBLIC_KEY = os.getenv('MARVEL_PUBLIC_KEY')
#PRIVATE_KEY = os.getenv('MARVEL_PRIVATE_KEY')

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

PARAMS = {
    'apikey': PUBLIC_KEY,
    'hash': '',
    'ts': '',
    'limit': PAGE_SIZE
}

CHARACTER_URL = 'http://gateway.marvel.com/v1/public/characters'

# VALID_CHARACTER_KEYS = ["id", "name", "description", "modified", "resourceURI",
#                         "thumbnail", "comics", "series", "stories", "events", "urls"]

VALID_CHARACTER_KEYS = list(json_characters_template_file.keys())

print (VALID_CHARACTER_KEYS)

def validate_json_params(response_results):

    for single_obj in response_results:

        result = numpy.in1d(VALID_CHARACTER_KEYS, list(single_obj.keys()))

        assert all(result) == True, "A parameter was missing from the Json response" \
                                    "Id with invalid params is: {id} ".format(id=single_obj['id'])

        assert len(VALID_CHARACTER_KEYS) == len(list(single_obj.keys())), "got more than expected"

def get_hash_and_ts_param():

    # hash_string = hashlib.md5("%s%s%s" % (unix_time_stamp, private_key, public_key)).hexdigest()
    unix_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
    marvel_hash_pre_hash = unix_time_stamp + PRIVATE_KEY + PUBLIC_KEY

    marvel_hash = hashlib.md5(marvel_hash_pre_hash.encode())

    marvel_hash_digest = marvel_hash.hexdigest()
    print (marvel_hash.digest())

    return {'ts': unix_time_stamp, 'hash': marvel_hash_digest}


def get_results_size(page_size):
    marvel_hash_and_params = get_hash_and_ts_param()
    PARAMS.update(marvel_hash_and_params)
    marvel_characters_response = requests.get(CHARACTER_URL, headers=HEADERS, params=PARAMS)

    total_results = json.loads(marvel_characters_response.text)
    total_results = int(total_results['data']['total'])

    print (total_results)

    number_of_loops = math.ceil(total_results/page_size)

    print (number_of_loops)
    return number_of_loops

def get_marvel_characters_json(page_size, total_pages):


    for i in range(total_pages):

        marvel_hash_and_params = get_hash_and_ts_param()

        PARAMS.update(marvel_hash_and_params)

        PARAMS.update({'offset': page_size * i})  # offset, how many records to skip

        # resp = requests.get(CHARACTER_URL, params)
        # print(f'Requested page xxxxxx {i} of {page_size} records')
        try:
            #logging.info("----------- Response Start -----------")

            marvel_characters_response = requests.get(CHARACTER_URL, headers=HEADERS, params=PARAMS)
            marvel_characters_response.raise_for_status()

            pretty_json = json.loads(marvel_characters_response.text)
            # print (json.dumps(pretty_json, indent=2))
            # print (pretty_json['data']['results'])

            validate_json_params(pretty_json['data']['results'])


            logging.info("Marvel character response: {response}".format(response=marvel_characters_response))
            # print(f'Requested page xxxxxx {i} of {page_size} records')


        except requests.exceptions.RequestException as e:
            raise type(e)("Marvel characters API repsonce is: {response}"
                  " Error is: {e}".format(response=marvel_characters_response, e=e))

    pass

def test_validate_characters_json_structure():

    # result = numpy.in1d(VALID_CHARACTER_KEYS ,["id", "name", "description", "resourceURI",
    #                     "thumbnail", "comics", "series", "stories", "events", "urls"])
    # print(result)
    # get_marvel_characters_json(PAGE_SIZE, get_results_size(PAGE_SIZE))
    get_marvel_characters_json(1, 1)


if __name__ == "__main__":
    pytest.main([__file__, "-x", "-k", "test_", "-v", "-s"])
