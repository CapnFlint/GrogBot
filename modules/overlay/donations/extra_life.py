#participant_url = "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participant&participantID=179842&format=json"

#donation_url = "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID=179842&format=json"

#donation['message']
#donation['donationAmount']
#donation['donorName']
#donation['createdOn']

last_donations = []
def get_latest_donation(self):
    url = "http://www.extra-life.org/index.cfm?fuseaction=donorDrive.participantDonations&participantID=179842&format=json"
    try:
        response = urllib2.urlopen(url)
        donations = json.load(response)[:10]

        for donation in donations:
            if donation not in last_donations:
                new_donation(self, donation)
        last_donations = donations

    except urllib2.URLError:
        return {}

def new_donation(donation):
    global connMgr
    if not donation['donorName']:
        donation['donorName'] = "Anonymous"
    connMgr.send_message("New donation from " + donation['donorName'] + " for " + str(donation['donationAmount']), screen=True, priority=1)
