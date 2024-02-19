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

"""Simple command-line example for Custom Search. Command-line application that does a search.

E6111 Project #1 - Richard Han, Aidana Imangozhina
"""
import warnings
import sys
import module
from googleapiclient.discovery import build

warnings.simplefilter('ignore')

def search_google(api_key, cse_id, search_query):
    """
    Perform search with Google Search JSON API
    """
    #Declare google search service with the api
    google_search_service = build("customsearch", "v1", developerKey=api_key)
    search_result = google_search_service.cse().list(q=search_query, cx=cse_id, num=10).execute()
    #We return the search result 
    return search_result.get('items', [])

def process_user_feedback(items):
    """
    User feedback function where we have them analyze the result
    """
    #Initialize relevant_items
    relevant_items = []  
    #Initialize counter to iterate through items
    i = 0
    #We do while loop until we have 10 results
    while i != 10:
        #We get the result with result, title, URL, summary, and Y/N
        message = (
            f"Result {i+1}:\n"
            f"Title: {items[i]['title']}\n"
            f"URL: {items[i]['link']}\n"
            f"Summary: {items[i]['snippet']}\n"
            "Relevant (Y/N)? "
        )
        #Ask for feedback from the user
        feedback = input(message).strip().lower()
        #If it's either y or yes
        if feedback in ('y', 'yes'):
            relevant_items.append(items[i])
            i+=1
        #If n or no, in this case
        elif feedback in ('n', 'no'):
            i+=1
            continue
        #If it's any other keys including enter key, we state it's wrong input
        else:
            print("Wrong input. Please choose yes (y) or no (n)")
    #We return the relevant items 
    return relevant_items

def print_initial_parameters(api_key, cse_id, query, target_precision):
    """
    Print initial search parameters to be displayed
    """
    #Below are initial paramters that we issue on command prompt
    print("\nParameters:")
    print(f"Client key  = {api_key}")
    print(f"Engine key  = {cse_id}")
    print(f"Query       = {query}")
    print(f"Precision   = {target_precision}")
    print("Google Search Results:")
    print("======================")

def feedback_summary(api_key, cse_id, query, precision, target_precision, new_words=[]):
    """
    Print feedback summary with updated augmentation information if it's available
    We reuse the feedback summary for code clarity and efficiency
    """
    # Initialize augmented new query with the current query
    new_query = query

    # If there are new words, append to new_query
    if new_words:
        new_query += " " + " ".join(new_words)

    #Following the format of sample server
    print("======================")
    print("FEEDBACK SUMMARY")
    print(f"Query {query}")
    #We issue precision as 1.0, 0.9, etc
    print(f"Precision: {precision:.1f}")
    #If precision is equal or greater than target, we state that desired precision is reached
    if precision >= target_precision:
        print("Desired precision reached. done.")
    #If not, we state it's below desired precision
    else:
        print(f"Still below the desired precision of {target_precision}")
        print("Indexing results ....")
        print("Indexing results ....")
        print("Augmenting by", " ".join(new_words) if new_words else "")

def main():
    usage_msg = "Usage: python3 main.py <google api key> <google engine id> <precision> <query>"
    if len(sys.argv) < 5:
        #This is the format of using the program. If less than the correct arg, we exit
        print(usage_msg)
        sys.exit(1)

    _, api_key, cse_id, precision, *query_parts = sys.argv
    if len(query_parts) > 1:
        # Print usage message in case query does not contain single or double quotation
        print(usage_msg)
        sys.exit(1)

    query = " ".join(query_parts)
    #We declare target precision for comparison
    target_precision = float(precision)

    #We start with initial parameters here to match the sample program
    print_initial_parameters(api_key, cse_id, query, target_precision)

    while True:
        items = search_google(api_key, cse_id, query)
        #If there are no items, we quit out of the program per specification
        if not items:
            print("No results found.")
            sys.exit(1)
            continue

        #We process the user feedback and store them in relevant items. Then calculate the precisions
        relevant_items = process_user_feedback(items)
        if items:
            precision_finished = len(relevant_items) / len(items)
        else:
            precision_finished = 0

        #If precision is empty, we output the precision as 0.0 and exit
        if precision_finished == 0.0:
            feedback_summary(api_key, cse_id, query, precision_finished, target_precision)
            print("Below desired precision, but can no longer augment the query")
            sys.exit(1)
        #If precision is greater or equal to target precision, we issue feedback summary with desired precision reached
        elif precision_finished >= target_precision:
            feedback_summary(api_key, cse_id, query, precision_finished, target_precision)
            break
        else:
            # Determine new words for augmentation step
            new_words = module.extract_new_words(original_query=query, relevant_docs=[item["snippet"] for item in relevant_items])
            feedback_summary(api_key, cse_id, query, precision_finished, target_precision, new_words)

            # Update query with new words for the next iteration
            # if new_words:
            #     query += " " + " ".join(new_words)   
            for word in new_words:
                query += " " +  word
            #Here, we issue parameter statements to follow the sample program         
            print_initial_parameters(api_key, cse_id, query, target_precision)

if __name__ == "__main__":
    main()
