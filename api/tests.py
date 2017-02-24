import datetime
import json

import requests
from django.test import TestCase

# Create your tests here.
# 黄金同步



def gold_sync():
    url = "http://web.juhe.cn:8080/finance/gold/shgold?v=&key=5465b4584fbdc8155b2693ae9fee2ac0"
    resp = requests.get(url, timeout=3, verify=False)
    result = json.loads(resp.content.decode())
    if result['error_code'] == 0:
        for entry in result['result']:
            for key in entry:
                if entry[key]['variety'] == "Au100g":
                    current_time = datetime.datetime.strptime(entry[key]['time'], '%Y-%m-%d %H:%M:%S')
                    # gold = Gold(type="GOLD",time=entry['time'], price=entry['latestpri']
                    #         , max_price=entry['maxpri'], min_price=entry['minpri'], yes_price=entry['yespri'], open_price=entry['openpri'],
                    #         total_vol=entry['totalvol'], limit=entry['limit'])
    return result



if __name__ == '__main__':
    print(gold_sync())
