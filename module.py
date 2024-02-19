import warnings
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from gensim.models import FastText
from sklearn.metrics.pairwise import cosine_similarity

warnings.simplefilter('ignore')

# read stop words from the project file
stop_words = []
# Open the file below
f = open('proj1-stop.txt', 'r')
# For word in f, we do the following
for word in f:
    # Remove leading or trailing whitespace from the word and add it to list
    stop_words.append(word.strip())

def remove_punctuation(input_string):
    """
    Clean the input string by removing punctuation signs.
    """
    # Create a translation table to remove punctuation
    translation_table = str.maketrans("", "", punctuation)
    # Apply the translation to the input string
    cleaned_string = input_string.translate(translation_table)
    return cleaned_string

def remove_stop_words(relevant_docs):
  """
  Remove stop words from the user-marked relevant documents.
  """
  # Stop word removal
  removed_sw = []
  #For s in relvant docs, we process the following by iterating
  for s in relevant_docs:
    # Convert document to lowercase and split into individual words
    words = s.lower().split()
    # We filter out stop words and punctuation
    filtered_words = [word for word in words if word not in stop_words]
    # We further filter words by removing punctuation from each word
    # We only keep words where punctuation removed version is non-empty then join back into the string
    filtered_words = [remove_punctuation(word) for word in filtered_words if remove_punctuation(word)]
    # Join filtered words back into a single string
    processed_string = " ".join(filtered_words)
     # Append the processed document to the list
    removed_sw.append(processed_string)
  return removed_sw

def calc_weights(original_query, relevant_docs):
  """
  Calculate weights of original query and relevant documents.
  """
  # Include the original query in the documents
  relevant_docs.append(original_query)
  # Remove stop words from documents
  docs_rem_sw = remove_stop_words(relevant_docs)
  
  # Vectorize
  # Initialize TF-IDF vectorizer and then fit_transform the processed documents
  vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r"(?u)\S\S+")
  X = vectorizer.fit_transform(docs_rem_sw)

  # Get cosine similarities for relevant_docs
  query_list = original_query.split()
  # Extract the features and sort by sum of weights
  dict_of_weights = {}
  # Convert TF-IDF matrix to dense format. Create a DataFrame for easier manipulation
  feature_names = vectorizer.get_feature_names_out()
  dense_tfidf_matrix = X.toarray()
  df_tfidf = pd.DataFrame(dense_tfidf_matrix, columns=feature_names)
  # For word in feature names, we do the loop
  for word in feature_names:
    # Avoid the word which is already in the query
    if word in query_list:
      continue
    if word in df_tfidf:
      dict_of_weights[word] = df_tfidf[word].sum()
  # We return dict of weights
  return dict_of_weights

def find_similarity(relevant_docs, query, words):
  res = {}
  # Train FastText model on the relevant documents
  model = FastText(sentences=relevant_docs)
  # Get embedding for the query
  word1_embedding = model.wv[query].reshape(1, -1)
  for w in words: # words with equal scores
    # Reshape the arrays to match the expected input shape of cosine_similarity
    word2_embedding = model.wv[w].reshape(1, -1)
    # Calculate cosine similarity
    similarity = cosine_similarity(word1_embedding, word2_embedding)[0][0]
    res[w] = similarity
  # We return res
  return res

def extract_new_words(original_query, relevant_docs):
  """
  Extract two new words for the new query.
  """
  # Extract new words from most similar document with weights
  dict_of_weights = calc_weights(original_query, relevant_docs)

  # Get the word with the highest sum of weights
  unique_values = set(dict_of_weights.values())
  max_value = max(unique_values)
  # Remove the highest value
  unique_values.remove(max_value)
  # Second word with highest weight in case weight values are not equal
  second_max_value = max(unique_values) if unique_values else None

  # Declare words with max weight and wordw with second max weight list
  words_with_max_weight = []
  words_with_second_max_weight = []
  # Match the maximum weight value to get the word from dictionary
  for k,v in dict_of_weights.items():
    # If current word's weight equals the maximum weight, we append word to the list of words with max weight
    if v == max_value:
      words_with_max_weight.append(k)
    # If current word's weight equals second maximum weight, we append word to the list of words with second max weight
    if v == second_max_value:
      words_with_second_max_weight.append(k)
  # Calculate similarity between query and words with the highest weights
  first_dict = find_similarity(relevant_docs, original_query, words_with_max_weight)
  second_dict = find_similarity(relevant_docs, original_query, words_with_second_max_weight)

  # Select the words with the highest similarity scores
  max_key = max(first_dict, key=lambda k: first_dict[k])
  # Pop the max key from first 
  first_dict.pop(max_key)
  # if length of first dict is 0 or empty
  if len(first_dict) == 0:
    # If first dictionary is empty, select the word with the highest score from second dictionary
    second_max_key = max(second_dict, key=lambda k: second_dict[k])
  else:
    # Else, we get the max of first dict and assign to second key max
    second_max_key = max(first_dict, key=lambda k: first_dict[k])
  # Return list containing the words with the highest and second highest cosine similarity score
  return [max_key, second_max_key]
