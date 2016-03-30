BH_OAuth
========
bullhorn.com REST API Python Client
-----------------------------------

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
