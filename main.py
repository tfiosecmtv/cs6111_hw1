#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple command-line example for Custom Search.

Command-line application that does a search.
"""

__author__ = "jcgregorio@google.com (Joe Gregorio)"

import pprint

from googleapiclient.discovery import build


def main():
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build(
        "customsearch", "v1", developerKey="AIzaSyBCa0Wc70pbXZGhPDAw6PN7TDzgJEqR-Gw"
    )

    res = (
        service.cse()
        .list(
            q="Luis Gravano",
            cx="24edf1bcc7aaa4d1b",
        )
        .execute()
    )
    dict = {}
    for i in res['items']:
        pprint.pprint(i['snippet'])
        pprint.pprint(i['title'])
        pprint.pprint(i['formattedUrl'])
    # pprint.pprint(i['snippet'])
    # pprint.pprint(len(res['items']))
    # pprint.pprint(res['items'][0]['title'])

if __name__ == "__main__":
    main()