import urllib2
import urllib
import json

'''
{'name','amount','message','type'}

type:
0 = standard tip
1 = extra-life
'''
def get_latest_tips():
    return get_extralife()

def get_extralife():
    url = "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID=179842&format=json"
    try:
        response = urllib2.urlopen(url)
        result = json.load(response)[:10]
        donations = []
        for donation in result:
            temp = {}
            temp['name'] = donation['donorName']
            temp['amount'] = donation['donationAmount']
            temp['message'] = donation['message']
            temp['type'] = 1
            donations.append(temp)
        return donations

    except urllib2.URLError:
        return {}
