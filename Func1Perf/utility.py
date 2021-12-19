import json
import os
import random
import linecache

BASE_URL = 'http://www.bing.com'
ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)


def get_agent():
    with open(os.path.join(BASE_DIR, r'Data\Browser_info.json'), 'rb') as f:
        browser_json = json.load(f)
        browser = browser_json['browsers']
        random_idx = random.randint(0, len(browser))
        if random_idx == 0:
            browser_name = "chrome"
        elif random_idx == 1:
            browser_name = "opera"
        elif random_idx == 2:
            browser_name = "firefox"
        elif random_idx == 3:
            browser_name = "internetexplorer"
        else:
            browser_name = "safari"
        random_agent = random.randint(0, len(browser[browser_name]))
    return browser[browser_name][random_agent]


def get_header():
    with open(os.path.join(BASE_DIR, r'Data\Header.json'), 'rb') as f:
        result = json.load(f)
        result['headers']['User-Agent'] = get_agent()
        return result['headers']


def get_query():
    data = {}
    random_idx = random.randint(1, 100)
    p = os.path.join(BASE_DIR, r'Data\Query.csv')
    print(p)
    line = linecache.getline(p, random_idx).rstrip('\n').split(',')
    data[line[0]] = line[1]
    return data


print(get_query())

