import sys
sys.path.append('./libs')

import requests
import json
import jwt
import time
import emoji
from auth0client import authorize
from workflow import Workflow, ICON_WEB, web

domain   = "alfred3-sample.auth0.com"
clientId = "bNTVEImdLBiZeC14E549I1TqGERT5O0A"
audience = "https://twitter.webtask/"
scopes = ['read_notifications', 'tweet', 'search']
webtaskUrl = "https://wt-abhishek_hingnikar-auth0_com-0.run.webtask.io/tweepy/tweet?webtask_no_cache=1"


def main(wf):
    if len(wf.args):
        status = wf.args[0]
    else:
        status = "This is a test"

    status = emoji.emojize(status, use_aliases=True)
    token = None

    try:
        token = wf.get_password('twitter-alfred')
        now = time.time()
        payload = jwt.decode(token)

        #Expired JWT
        if payload.exp < now:
            token = None

    except:
        pass
    ## Authenticate
    if token is None:
        (status_code, message, response) = authorize(
            client_id=clientId,
            domain=domain,
            connection="twitter",
            audience=audience
        )
        if not status_code is 200:
            print status_code, message, response
            return
        token = response["access_token"]
        wf.save_password('twitter-alfred', token)

    headers = {
        "content-type": "application/json",
        "Authorization": ("Bearer %s" % token)
    }

    response = requests.post(
        webtaskUrl,
        data=json.dumps({
            "status": status
        }),
        headers=headers
    )

    print response.json()



if __name__ == u"__main__":
     wf = Workflow()
     sys.exit(wf.run(main))
