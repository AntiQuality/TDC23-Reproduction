import requests
import json
import uuid
from sentencepiece import SentencePieceProcessor

# 1. Setup Azure API Key
# Add your key and endpoint
key = ""
# You need to full the key string with your own Azure API Key.
endpoint = "https://api.cognitive.microsofttranslator.com"
# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "eastus"
path = '/translate'
constructed_url = endpoint + path

high_resource_languages_updated = [
    'en', 'zh-Hans', 'de', 'fr', 'es', 'ru', 'ja', 'ar', 'pt', 'pt-pt', 'it', 'nl', 'tr', 
    'pl', 'ko', 'vi', 'hi', 'zh-Hant'
]                                   # 18
mid_resource_languages_updated = [
    'bs', 'bg', 'cs', 'da', 'fi', 'el', 'hu', 'id', 'nb', 'ro', 'sr-Cyrl', 'sr-Latn', 'sk', 
    'sl', 'sv', 'ta', 'th', 'uk', 'ur', 'he', 'ms', 'bn', 'ca', 'hr'
]                                   # 24
low_resource_languages_updated = [
    'af', 'sq', 'am', 'hy', 'az', 'ba', 'eu', 'yue', 'lzh', 'sn', 'prs', 'dv', 'et', 'fo', 
    'fj', 'fil', 'gl', 'ka', 'gu', 'ht', 'ha', 'mww', 'is', 'ig', 'ikt', 'iu', 'iu-Latn', 
    'ga', 'kn', 'kk', 'km', 'rw', 'tlh-Latn', 'tlh-Piqd', 'ku', 'kmr', 'ky', 'lo', 'lv', 
    'lt', 'ln', 'dsb', 'lug', 'mk', 'mai', 'mg', 'ml', 'mt', 'mi', 'mr', 'mn-Cyrl', 
    'mn-Mong', 'my', 'ne', 'nya', 'or', 'ps', 'fa', 'pa', 'otq', 'run', 'sm', 'st', 'nso', 
    'tn', 'sd', 'si', 'so', 'sw', 'ty', 'tt', 'te', 'bo', 'ti', 'to', 'tk', 'ug', 'uz', 
    'cy', 'xh', 'yo', 'yua', 'zu', 'as', 'fr-ca', 'gom', 'hsb'
]                                   # 87
spe_resource_languages_updated = ['el', 'da', 'bn', 'ta', 'ca']
spe_resource_languages_updated_weighted = ['el', 'da', 'bn', 'bn', 'ca', 'el', 'da', 'bn', 'ca', 'ca']
lang_list = mid_resource_languages_updated + mid_resource_languages_updated + ['ca', 'bn']
# lang_list is the target language list with 50 kinds of language

# 2. Function: Send Translation Requirement
def translate(id, text, from_lang, to_lang):
    print(f'{id}: Translate "{text}" from {from_lang} to {to_lang} now...')
    params = {
        'api-version': '3.0',
        'from': f'{from_lang}',
        'to': f'{to_lang}'
    }
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    body = [{
        'text': f'{text}'
    }]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

sp = SentencePieceProcessor(model_file="tokenizer.model")

# 3. Count the number of tokens
def token_calc(x):
    tokens = sp.EncodeAsIds(x)
    return len(tokens)



LIMIT_TOKEN_NUM = 250

from_lang = 'en'
test_case_path = "./behaviors.json"
test_cases = json.load(open(test_case_path, 'r', encoding='utf-8'))
generations = {}

CASE_NUMBER = 50

i = 0
for behavior in test_cases:
    print(f"Generating for behavior {i+1}/{len(test_cases)}: {behavior}")
    generations[behavior] = []
    for j in range(0, CASE_NUMBER):
        trans_target = behavior
        to_lang = lang_list[j]
        translated = translate(j, trans_target.replace('\n',' '), from_lang, to_lang)
        while (token_calc(translated) > LIMIT_TOKEN_NUM):
            translated = translated[:len(translated)-1]
        print(f'LEN: {token_calc(translated)} with \"{translated}\".')
        generations[behavior].append(f'Answer in {to_lang} language: {translated}.')
    i = i+1

generations_path = "./test_cases.json"
with open(generations_path, 'w', encoding='utf-8') as file:
    json.dump(generations, file, ensure_ascii=False, indent=4)