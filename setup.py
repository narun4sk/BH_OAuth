#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = "bh_oauth",
    version = "2.0.0",
    author = "Narūnas Krasauskas",
    author_email = "narun4sk@gmail.com",
    url = "https://github.com/narunask/BH_OAuth",
    download_url = "https://github.com/narunask/BH_OAuth/archive/master.zip",
    keywords = ["bullhorn", "rest", "client"],
    install_requires = ["requests>=2.9.1",],
    package_dir = {'': 'BH_OAuth_py2'},
    py_modules = ["bh_oauth",],
    data_files=[("", ["LICENSE"]),],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        ],
    description = "bullhorn.com REST API Client",
    long_description = """\
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
)