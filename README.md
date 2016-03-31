## bullhorn.com REST API Python Client

*Install*:

    # pip install -U bh_oauth

*Dependencies*:

- [requests][requests] - HTTP for Humans

*Features*:

- Automatically refresh `rest_token` / `url` if `access_token` has expired.
- Search the following entity types given a string containing search terms.

*Quick Example*:

    from bh_oauth import BHRest

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

[requests]: http://docs.python-requests.org/en/master/user/install/#install "HTTP for Humans"
