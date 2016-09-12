import urllib
import json

import requests

requests.packages.urllib3.disable_warnings()

'''
{"params":"query:capn_flint 2k crew
hitsPerPage:12
attributesToRetrieve:["name","url","tippingpoint","amount_ordered","primary_pic_url","secondary_pic_url","endcost","enddate"]
page:0"}
'''

def get_orders(query, international = False):
    try:
        query = urllib.quote(query)
        headers = {'content-type': 'application/json'}
        url = 'https://xnf09ccdo4-dsn.algolia.net/1/indexes/site_wide_search_index_production/query'
        data = {'params':'query=' + query + '&hitsPerPage=12&attributesToRetrieve=%5B%22name%22%2C%22url%22%2C%22tippingpoint%22%2C%22amount_ordered%22%2C%22primary_pic_url%22%2C%22secondary_pic_url%22%2C%22endcost%22%2C%22enddate%22%5D&page=0'}
        params = {'X-Algolia-API-Key': '5cf4b4f788d542e9e1661cb977480f0dcb5acfdae52786e3bf9593ba8da3ddd4',
                  'X-Algolia-Application-Id': 'XNF09CCDO4',
                  'X-Algolia-TagFilters': '-relaunched'}

        r = requests.post(url, params=params, data=json.dumps(data), headers=headers)
        count = r.json()['hits'][0]['amount_ordered']
        if international:
            count = count + r.json()['hits'][1]['amount_ordered']
        return count

    except urllib2.URLError:
        print "error"
        return {}
