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

"""
E6111 Project #1 - Richard Han, Aidana Imangozhina
"""

import sys
import random
from googleapiclient.discovery import build

def search_google(api_key, cse_id, search_query):
    """
    Perform search with Google Search JSON API.

    """
    google_search_service = build("customsearch", "v1", developerKey=api_key)

    # Make search request 
    search_result = google_search_service.cse().list(
        q=search_query,  
        cx=cse_id,       
        num=10           
    ).execute()

    items = search_result.get('items', [])

    return items

def perform_user_feedback(items):
    """
    User feedback function
    """
    relevant_items = []  
    for index, item in enumerate(items, start=1):
        message = (
            f"Result {index}:\n"
            f"Title: {item['title']}\n"
            f"URL: {item['link']}\n"
            f"Summary: {item['snippet']}\n"
            "Relevant (Y/N)? "
        )
        
        feedback = input(message).strip().lower()
        
        if feedback == 'y':
            relevant_items.append(item)
    
    return relevant_items

def add_randomword(query):
    """
    Add a random word to the query to refine it for now. TODO: This will be replaced by step 4.
    """
    random_words = ['sf', 'los angeles', 'california', 'newyork']
    random_word = random.choice(random_words)
    new_query = query + " " + random_word
    print(f"Augmenting by {random_word}")
    return new_query, random_word

def feedback_summary(api_key, cse_id, query, precision, target_precision, augmentation):
    """
    Summary of feedback in the command prompt.
    """
    print("\nFEEDBACK SUMMARY")
    print(f"Query {query}")
    print(f"Precision {precision:.2f}")
    print(f"Still below the desired precision of {target_precision}")
    print("Indexing results ....")
    print("Indexing results ....")
    if augmentation:  
        print(f"Augmenting by {augmentation}")
    else:
        print("No augmentation performed.")
    print("Parameters:")
    print(f"Client key  = {api_key}")
    print(f"Engine key  = {cse_id}")
    print(f"Query       = {query}")
    print(f"Precision   = {target_precision}")
    print("Google Search Results:")
    print("======================")

def main():
    """
    Execute main function.
    """
    if len(sys.argv) < 5:
        print("Usage: script.py <google api key> <google engine id> <precision> \"<query>\"")
        sys.exit(1)

    _, api_key, cse_id, precision, *query_parts = sys.argv
    query = " ".join(query_parts)
    target_precision = float(precision)

    print("Parameters:")
    print(f"Client key  = {api_key}")
    print(f"Engine key  = {cse_id}")
    print(f"Query       = {query}")
    print(f"Precision   = {precision}")
    print("Google Search Results:")
    print("======================")


    #Placenolder for augmented word
    augmentation = ""  

    #TODO: This needs to be replaced with step4
    #Currently, it looks for new augmented words to keep searching
    #TODO: Add in more error handling
    while True:
        items = search_google(api_key, cse_id, query)
        if not items:
            print("No results found.")
            query, augmentation = add_randomword(query)
            continue

        relevant_items = perform_user_feedback(items)
        precision_finished = len(relevant_items) / len(items)
        print(f"Precision achieved: {precision_finished:.2f}")

        if precision_finished >= target_precision:
            print("Desired precision reached. Done.")
            break
        else:
            print("Desired precision not reached. Refining your query.")
            query, augmentation = add_randomword(query)
            feedback_summary(api_key, cse_id, query, precision_finished, target_precision, augmentation)

if __name__ == "__main__":
    main()

