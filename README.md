# BH_OAuth
bullhorn.com REST API Python Client

*Dependencies*:

- [requests](http://docs.python-requests.org/en/master/user/install/#install)

*Quick Example*

    client = "Bullhorn OAuth Client ID"
    secret = 'Bullhorn OAuth Client Secret'
    username = "Bullhorn Username"
    password = "Bullhorn Password"

    bhr = BHRest(client=client, secret=secret, usr=username, pwd=password)
    print bhr.access_token
    print bhr.find(query="+12345678")

*Features*:

- Automatically refresh `rest_token/url` if `access_token` has expired.
- Search the following entity types given a string containing search terms.
