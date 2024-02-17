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

```
```

## Detailed description of query-modification method

```
```
1. We referred to tf-idf embedding and cosine similarity techniqes from the lecture. We clean up the user marked relevant queries using the stop words file from the project page and remove any punctuation signs from the documents.
2. We identify the most similar document by calculating the cosine similarity of each user-marked relevant document with the previous query. 
3. To get the cosine similarity of relevant documents, each relevant document is embedded using tf-idf vectorizer technique that we saw during the lecture. We used the library function from "sklearn" and we used on that all the relevant documents and the previous query. 
4. Now that we have the embeddings, we can calculate cosine similarity for each embedded relevant document with the previous query. Cosine similarity is also calculated using the library function from "sklearn".
5. We extract feature names, e.g. unique words that were in the relevant documents and create a dataframe using the words as columns. Each row is the score of the features calculated for each relevant document.
6. We sum all the rows to get the overall score for each word (feature) to see their overall presence in all relevant documents.
7. We iterate through the features (unique words) and if they appear in the sentence which has the highest cosine similarity, we add them to the newly initialized dictionary (key: word, value: overall score or sum of rows for that word).
8. From that dictionary we get two words with the highest score. If the most similar document has one word we return only one word, but this scenario is highly unlikely and was considered for error handling.
9. If we have multiple words with the equal highest score we return by length. The ordering for returning words: highest score and then the longest word. For example, covid19 and vaccination have equal scores, we return "vaccination covid19". We always return two words to append to the previous query unless the most similar document contains only word (very unlikely scenario).

## NON - HTML files






