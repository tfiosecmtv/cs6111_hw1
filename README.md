# E6111 Project 1 
This is our README of our project 1. We achieve over 0.9 threshold of precision each time with our query augmentation method. 

## Authors
Richard Han (dh3062)

Aidana Imangozhina (ai2523)

## Files we're submitting
main.py

module.py

proj1-stop.txt

transcript.pdf

## Getting Started

### Usage/How to run
To run our project in our server, first, ssh guest-user@35.229.30.245. Password is guest-user.

The program is already set up for you to run and execute.

Run the project using command: 
```
/home/ai2523/run <google api key> <google engine id> <precision> <query>
```

### Keys / EngineID

Google API key = AIzaSyDU0M8qHB6gcorISsUwROoEEINdkLxL-6g 
Google Engine ID = 75a89ae4175564bf3
Precision = 0.9

### Clear description of the internal design of your project

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

The Google Search API we utilize handles non-HTML files by indexing through the content and making it searchable alongside traditional web pages. This feature enhances the ability to search and retrieve a wide range of information from the web through the API. For example, when we search for columbia ppt file, using our program, it was able to find the exact ppt with exact wording summary extracted from non html file, ppt in this case.

```
Title: FileNewTemplate
URL: https://engineering.columbia.edu/files/engineering/template_presentations-FY16-102615.ppt
Summary: Content slide: white background, top tab; Content slide: black background, white tab. TRANSCENDING DISCIPLINES, TRANSFORMING LIVES. 3 | Presentation Title ...
```

Furthermore, we further searched through Columbia pdf files, and we are able to obtain pdf file with comprehensive summary indicated from the search.

```
Title: COLUMBIA-SUICIDE SEVERITY RATING SCALE (C-SSRS)
URL: https://cssrs.columbia.edu/wp-content/uploads/C-SSRS_Pediatric-SLC_11.14.16.pdf
Summary: Definitions of behavioral suicidal events in this scale are based on those used in The Columbia Suicide History. Form, developed by John Mann, ...
```

## Detailed description of query-modification method


1. We referred to tf-idf embedding and cosine similarity techniques from the lecture. We clean up the user marked relevant queries using the stop words file from the project page and remove any punctuation signs from the documents.
2. We use tf-idf embedding from "scikit-learn" to get vector representation and weights of the documents and query.
3. For each separate word or feature in the vectorizer we create a dataframe and store their score for each document. However, we do not include query since we are considering new words which are not in the query to avoid duplicates.
4. We extract feature names, e.g. unique words that were in the relevant documents and create a dataframe using the words as columns. Each row is the score of the features calculated for each relevant document.
6. We sum all the rows to get the overall score for each word (feature) to see their overall presence in all relevant documents.
7. We create two dictionaries (key: word, value: score) for documents with the highest and second highest score. We iterate through the features (unique words), and put them to the dictionary if their scores are equal to the highest or the second highest score.
8. We order words based on their score. If we have multiple words with the highest score or only one element with the first highest score and multiple elements with the second highest score, we need to decide the order using cosine similarity between words and the previous query.
9. To decide the ordering we use FastText model from the gensim library to get vector representation for each word, and we use relevant documents as training data. We chose this model since gensim library includes Word2Vec representation to understand context better which is handy for similarity analysis, and FastText is optimized to get word embeddings and is a smaller model given the scope of the project, and we're still getting optimal results. After getting vector representation we calculate cosine similarity for each word and the previous query from "scikit-learn".







