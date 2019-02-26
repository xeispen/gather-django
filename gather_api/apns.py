import json
import jwt
import time
from hyper import HTTPConnection


def post(token):
    ALGORITHM = 'ES256'
    APNS_KEY_ID =
    APNS_AUTH_KEY =
    TEAM_ID = 
    BUNDLE_ID = 'com.px.gather'
    path = '/3/device/{0}'.format(token)

    f = open(APNS_AUTH_KEY)
    secret = f.read()

    token = jwt.encode(
        {
            'iss': TEAM_ID,
            'iat': time.time()
        },
        secret,
        algorithm= ALGORITHM,
        headers={
            'alg': ALGORITHM,
            'kid': APNS_KEY_ID,
        }
    )


    request_headers = {
        'apns-expiration': '0',
        'apns-priority': '10',
        'apns-topic': BUNDLE_ID,
        'authorization': 'bearer {0}'.format(token.decode('ascii'))
    }

        # Open a connection the APNS server
    conn = HTTPConnection('api.sandbox.push.apple.com:443')

    payload_data = {'aps':
                        {'alert' : {'title' : 'Title',
                                    'subtitle' : 'subtitle',
                                    'body' : 'body'},
                         'sound' : 'default',
                         'badge' : 1
                        }
                    }

    payload = json.dumps(payload_data).encode('utf-8')

    # Send our request
    conn.request(
        'POST',
        path,
        payload,
        headers=request_headers
    )
    resp = conn.get_response().read()
    print(resp)
    print("Sent push notification...")
