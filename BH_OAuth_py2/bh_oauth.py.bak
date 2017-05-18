#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
BSD 3-Clause License::
--------------------

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of BH_OAuth nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Copyright (c) 2016 Narunas K. All rights reserved.

BH_OAuth
========
bullhorn.com REST API Client
----------------------------

*Dependencies*:

- `requests`_ - HTTP for Humans

*Quick Example*::

    auth = dict(
        client = "Bullhorn OAuth Client ID",
        secret = 'Bullhorn OAuth Client Secret',
        username = "Bullhorn Username",
        password = "Bullhorn Password")

    bhr = BHRest(**auth)
    bhr._auth_url = "https://auth9.bullhornstaffing.com/oauth"
    bhr._rest_url = "https://rest9.bullhornstaffing.com/rest-services"

    print bhr.access_token
    print bhr.find(query="+12345678")

*Features*:

- Automatically refresh `rest_token/url` if `access_token` has expired.
- Search the following entity types given a string containing search terms.

.. _requests: http://docs.python-requests.org/en/master/user/install/#install

"""

import urlparse
from datetime import datetime, timedelta

import requests

# Bullhorn Base URLs
AUTH_URL = "https://auth.bullhornstaffing.com/oauth"
REST_URL = "https://rest.bullhornstaffing.com/rest-services"


class BHAuth(object):
    """ Obtain Bullhorn OAuth authorization code and access token. """
    # Bullhorn OAuth Base URL
    _auth_url = AUTH_URL

    def __init__(self, client, secret, usr, pwd):
        # Bullhorn OAuth Client ID
        self.client = client
        # Bullhorn OAuth Client Secret
        self.secret = secret
        # Bullhorn Username
        self.usr = usr
        # Bullhorn Password
        self.pwd = pwd
        self.refresh = False
        self._auth_code = None
        self._access_token = None
        self._expired = None

    @property
    def auth_code(self):
        if self._auth_code is None:
            self.get_auth_code()
        return self._auth_code

    @property
    def access_token(self):
        if self._access_token is None:
            self.get_access_token()
        elif self.expired and self._access_token:
            self.get_access_token(refresh=True)
        return self._access_token

    @property
    def auth_params(self):
        return dict(
            client_id=self.client,
            response_type="code",
            username=self.usr,
            password=self.pwd,
            action="Login")

    @property
    def access_params(self):
        if not self.auth_code:
            return {}
        return dict(
            client_id=self.client,
            client_secret=self.secret,
            code=self.auth_code,
            grant_type="authorization_code")

    @property
    def expired(self):
        """ Return True if access_token has expired. """
        if self._expired is None:
            return False
        elif not isinstance(self._expired, datetime):
            return True
        now = datetime.now()
        if now >= self._expired:
            return True
        return False

    @property
    def refresh_params(self):
        if (isinstance(self._access_token, dict) and
                all(x in self._access_token for x in ["access_token", "refresh_token"])):
            return dict(
                client_id=self.client,
                client_secret=self.secret,
                refresh_token=self._access_token["refresh_token"],
                grant_type="refresh_token")
        return {}

    def get_auth_code(self):
        """ Obtain authorization code from the Bullhorn server. """
        url = self._auth_url + "/authorize"
        params = self.auth_params
        req = requests.get(url, params=params)
        response_url = req.url
        response_query = requests.utils.urlparse(response_url).query
        query_dict = urlparse.parse_qs(response_query)
        if query_dict.get("code"):
            self._auth_code = query_dict["code"][0]
        else:
            self._auth_code = ""
        return self._auth_code

    def get_access_token(self, refresh=None):
        """ Obtain access token from the Bullhorn server.
            The POST response contains an access token that you use in REST API /login requests
            to obtain a Bullhorn session token and a base REST URL.
            The access token is valid for 10 minutes.
        """
        url = self._auth_url + "/token"
        # If refresh is not explicitly declared, set it to the instance variable
        if refresh is None:
            refresh = self.refresh
        if not refresh:
            params = self.access_params
        else:
            params = self.refresh_params
        req = requests.post(url, params=params)
        self.access_token_url = req.url
        try:
            response_dict = req.json()
        except Exception as err:
            print err
            response_dict = {}
            self.refresh = False
        if 'expires_in' in response_dict:
            now = datetime.now()
            # Subtract 5 seconds just to be in the safe zone
            exp = int(response_dict['expires_in']) - 5
            self._expired = now + timedelta(seconds=exp)
        if all(x in response_dict for x in ["access_token", "refresh_token"]):
            self.refresh = True
        self._access_token = response_dict
        return self._access_token

    @property
    def valid_atoken(self):
        if self.access_token and not self.access_token.get("error"):
            return True
        return False


class BHRest(BHAuth):
    """ Make Bullhorn REST queries. """
    _rest_url = REST_URL
    # version query parameter: * == latest version, 2.0 == current version
    version = "*"

    def __init__(self, *a, **kw):
        super(BHRest, self).__init__(*a, **kw)
        self._rest_login = None

    def _get_rest_credentials(self):
        if self._rest_login is None:
            self.rest_login()
        elif self.expired and self.access_token:
            # If access_token has expired - refresh token and acquire new rest_token/url
            self.get_access_token(refresh=True)
            self.rest_login()

    @property
    def rest_token(self):
        self._get_rest_credentials()
        return self._rest_login.get("BhRestToken")

    @property
    def rest_url(self):
        self._get_rest_credentials()
        return self._rest_login.get("restUrl")

    @property
    def login_params(self):
        if (isinstance(self.access_token, dict) and
                "access_token" in self.access_token):
            return dict(
                version=self.version,
                access_token=self.access_token["access_token"])
        return {}

    def rest_login(self, v=None):
        """ Obtain session key (rest_token) and base URL (rest_url) from the Bullhorn server. """
        if v:
            self.version = v
        url = self._rest_url + "/login"
        params = self.login_params
        req = requests.get(url, params=params)
        try:
            response_dict = req.json()
        except Exception as err:
            print err
            self._rest_login = {}
        self._rest_login = response_dict
        return self._rest_login

    def find(self, query="", meta="full", showEditable="true", countPerEntity=""):
        """ Searches the following entity types given a string containing search terms:
            - ClientContact
            - JobOrder
            - Candidate
            - ClientCorporation
            - Lead (if leadsAndOpportunitiesEnabled = true)
            - Opportunity (if leadsAndOpportunitiesEnabled = true)
            To search through the phone numbers start query with the "+" and append last 8 digits.
        """
        if not all([self.rest_token, self.rest_url]):
            return {}
        url = self.rest_url + "/find"
        params = dict(
            BhRestToken=self.rest_token,
            query=query,
            meta=meta,
            showEditable=showEditable,)
        req = requests.get(url, params=params)
        try:
            response_dict = req.json()
        except Exception as err:
            print err
            response_dict = {}
        return response_dict.get("data")


if __name__ == "__main__":
    auth = dict(
        client = "Bullhorn OAuth Client ID",
        secret = 'Bullhorn OAuth Client Secret',
        username = "Bullhorn Username",
        password = "Bullhorn Password")

    bhr = BHRest(**auth)
    bhr._auth_url = "https://auth9.bullhornstaffing.com/oauth"
    bhr._rest_url = "https://rest9.bullhornstaffing.com/rest-services"

    print bhr.access_token
    print bhr.find(query="+12345678")
