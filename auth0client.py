# -*- coding: utf-8 -*-
import webbrowser
import hashlib
import base64
import urllib
import urlparse
import BaseHTTPServer
import socket
import requests
import json
import httplib
from uuid import uuid4


# This way of handling authentication is inspried by Google's OAuth2Client library

class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    """A server to handle OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into query_params and then stops serving.
    """
    query_params = {}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """A handler for OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into the servers query_params and then stops serving.
    """

    def do_GET(self):
        """Handle a GET request.

        Parses the query parameters and prints a message
        if the flow has completed. Note that we can't detect
        if an error occurred.
        """
        self.send_response(httplib.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        query = self.path.split('?', 1)[-1]
        query = dict(urlparse.parse_qsl(query))
        self.server.query_params = query
        self.wfile.write(
            b"""
                <html>
                    <head>
                        <title>Authentication Status</title>
                    </head>
                    <body>
                        <p>The authentication flow has completed. You can close this tab now</p>
                    </body>
                </html>
            """
        )

    def log_message(self, format, *args):
        """Do not log messages to stdout while running as cmd. line program."""

def get_authorize_url(**kwargs):

    if kwargs is None:
        raise ValueError("you must pass authorization parameters to this call, based on Auth0's docs at")

    domain = kwargs.pop('domain', None)

    if domain is None:
        raise ValueError("You must pass domain=yourtenant.auth0.com")

    return "https://%s/authorize?%s" % (domain, urllib.urlencode(kwargs))

def base64urlEncode(data):
    return base64.urlsafe_b64encode(data).rstrip("=")

def hashSHA256(secret):
    return hashlib.sha256(secret).digest()


def getHashAndSecret():
    secret = base64urlEncode(uuid4().hex)
    hashed = base64urlEncode(hashSHA256(secret))
    return (hashed, secret)

def authorize(**kwargs):

    for port in range(3044, 3048):
        try:
            httpd = ClientRedirectServer(('', port), ClientRedirectHandler)
        except socket.error:
            pass
        else:
            success = True
            break


    (challenge, secret) = getHashAndSecret()

    redirect_uri = 'http://localhost:%s/callback' % str(port)

    print "Challenge: %s" % challenge
    print "Secret: %s" % secret

    kwargs["code_challenge"] = challenge
    kwargs["code_challenge_method"] = "S256"
    kwargs["response_type"] = "code"
    kwargs["redirect_uri"] = redirect_uri
    url = get_authorize_url(**kwargs)
    print "Opening %s in browser, please authenticate in browser" % url
    webbrowser.open(url)

    httpd.handle_request()

    if "error" in httpd.query_params:
        return (401, httpd.query_params["error"], httpd_query_params["error_description"])

    if "code" in httpd.query_params:
        code = httpd.query_params['code']
        token_endpoint = "https://%s/oauth/token" % kwargs["domain"]
        payload = {
            "grant_type": "authorization_code",
            "client_id": kwargs["client_id"],
            "redirect_uri": redirect_uri,
            "code_verifier": secret,
            "code": code
        }

        headers = {
            "content-type": "application/json"
        }

        print json.dumps(payload)
        response = requests.post(
            token_endpoint,
            data=json.dumps(payload),
            headers=headers
        )
        print response.status_code

        json_response = response.json()

        if not response.status_code is requests.codes.ok:
            return (response.status_code, "Error Exchanging Token", json_response)

        return (200, "Successful", json_response)
