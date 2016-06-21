## bullhorn.com REST API Python Client

*Install*:

    # pip install -U bh_oauth

*Dependencies*:

- [requests][requests] - HTTP for Humans

*Features*:

- Automatically refresh `rest_token` / `url` if `access_token` has expired.
- Search the following entity types given a string containing search terms:
  - ClientContact
  - JobOrder
  - Candidate
  - ClientCorporation
  - Lead (if leadsAndOpportunitiesEnabled = true)
  - Opportunity (if leadsAndOpportunitiesEnabled = true)
  - To search through the phone numbers start query with the "+" and append last 8 digits.

*Quick Example*:

    from bh_oauth import BHRest

    auth = dict(
        client = "Bullhorn OAuth Client ID",
        secret = 'Bullhorn OAuth Client Secret',
        usr = "Bullhorn Username",
        pwd = "Bullhorn Password")

    bhr = BHRest(**auth)
    bhr._auth_url = "https://auth9.bullhornstaffing.com/oauth"
    bhr._rest_url = "https://rest9.bullhornstaffing.com/rest-services"

    print bhr.access_token
    print bhr.find(query="+12345678")

[requests]: http://docs.python-requests.org/en/master/user/install/#install "HTTP for Humans"
