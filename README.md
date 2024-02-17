# E6111 Project 1 
This is our README of our project 1. We achieve over 0.9 threshold of precision each time with our query augmentation method. 
We have commented the code with detail with explanation for each functions and commands.  

## Authors
Richard Han(dh3062)

Aidana Imangozhina(ai2523)

## Files we're submitting
main.py

module.py

proj1-stop.txt

transcript.pdf

## Getting Started

### Usage/How to run
To run our project in our server, first, ssh guest-user@35.229.30.245. Password is same as username.

The program is already set up for you to run and execute.

Run the project using command: 
```
/home/ai2523/run <google api key> <google engine id> <precision> <query>
```

### Keys / EngineID

Google API key = AIzaSyDU0M8qHB6gcorISsUwROoEEINdkLxL-6g 

Google Engine ID = 75a89ae4175564bf3

Precision = 0.9 #This value can be changed by user.

### Clear description of the internal design of our project

Search Google Function: We have the function search google with api key, cse_id, and search query parameter to search and return top 10 results utilizing Google Custom Search JSON API. 

Process User Feedback: Utilizing process user feedback function, We then process feedback from the user to see if they find the search relevant or not. This can be marked with yes, y, no, n. If any other keys are entered, we let the user know that the key is not valid, and prompts the user to use yes, y, no, or no key to proceed. Enter key is also supplied with invalid prompt. It iterates through the results, asking the user to mark each as relevant or not, and collects the relevant items for further processing. 

Print Initial Parameter: We also have the print_initial_parameters function that displays the initial search parameters before executing the search, including the API and engine keys, query, and target precision.

Feedback Summary: We print a summary of the search feedback, including the current query, achieved precision, and whether the target precision has been met. If new words are identified for query augmentation, they are also displayed. We follow the sample implementation to ensure that all details output is matched on our instance.

We have the main function and we begin by validating command line arguments to ensure the required parameters are provided by the user. It extracts these parameters: the Google API key, Custom Search Engine ID, target precision, and the search query. If the user does not supply the needed format, they will be prompted with message indicating to run in this format. We also print the initial search parameters and we enter a loop where it performs the search, processes user feedback, and refines the search iteratively.

Using search_google(), we get search results based on the current query. Through process_user_feedback(), we gather user input on the relevance of each search result with result, title, URL and summary. User can also go into URL to see if link is relevant or not. After that is completed, we also determine the precision of the current search results based on user feedback and decide whether further augmentation and refinement is needed. If the precision achieved based on user feedback is below the target precision we set, we identify new words to augment the query using our algorithm and update the query accordingly. We continue this process until the precision meets or exceeds the target. Another instance is when the precision is 0.0 at any given point, we exit out of the program. All our runs achieved over 0.9 precision on our first iteration run.


## NON - HTML files






