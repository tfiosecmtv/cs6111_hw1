import pprint
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# read stop words from the project file
stop_words = []
f = open('proj1-stop.txt', 'r')
for word in f:
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
  for s in relevant_docs:
    words = s.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    filtered_words = [remove_punctuation(word) for word in filtered_words if remove_punctuation(word)]
    processed_string = " ".join(filtered_words)
    removed_sw.append(processed_string)
  return removed_sw

def calc_weights(original_query, relevant_docs):
  """
  Calculate weights of original query and relevant documents.
  """
    
  docs_rem_sw = remove_stop_words(relevant_docs)

  # Vectorize
  vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=r"(?u)\S\S+")
  X = vectorizer.fit_transform(docs_rem_sw)
  query_embedding = vectorizer.transform([original_query]) # no need to relearn

  # Get cosine similarities for relevant_docs
  cosine_similarities = query_embedding.dot(X.T).toarray()[0]
  highest_similarity_index = cosine_similarities.argmax()
  # Get the similarity score
  most_similar = docs_rem_sw[highest_similarity_index].split()
  query_list = original_query.split()
  # Extract the features and sort by sum of weights
  dict_of_weights = {}
  feature_names = vectorizer.get_feature_names_out()
  dense_tfidf_matrix = X.toarray()
  df_tfidf = pd.DataFrame(dense_tfidf_matrix, columns=feature_names)
  for word in most_similar:
    # Avoid the word which is already in the query
    if word in query_list:
      continue
    if word in df_tfidf:
      dict_of_weights[word] = df_tfidf[word].sum()
  return dict_of_weights

def extract_new_words(original_query, relevant_docs):
  """
  Extract two new words for the new query.
  """
  # Extract new words from most similar document with weights
  dict_of_weights = calc_weights(original_query, relevant_docs)

  # Get the word with the highest sum of weights
  unique_values = set(dict_of_weights.values())
  max_value = max(unique_values)
  unique_values.remove(max_value)
  # Second word with highest weight in case weight values are not equal
  second_max_value = max(unique_values) if unique_values else None

  words_with_max_weight = []
  # Match the maximum weight value to get the word from dictionary
  for k,v in dict_of_weights.items():
    if v == max_value:
      words_with_max_weight.append(k)
  words_with_second_max_weight = []
  # In the event if the relevant document only has one word
  if len(words_with_max_weight) == 1:
    if second_max_value is not None:
      for k,v in dict_of_weights.items():
        if v == second_max_value:
          words_with_second_max_weight.append(k)
    else:
      return words_with_max_weight
    sorted_list = sorted(words_with_second_max_weight)
    return [words_with_max_weight[0], sorted_list[-1]]
  # Return two new words to append to the original query
  sorted_list = sorted(words_with_max_weight)
  return [sorted_list[-1], sorted_list[-2]]