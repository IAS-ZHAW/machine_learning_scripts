# -*- coding: utf-8 -*-
import time
import json
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
from scipy.spatial.distance import pdist, squareform
from mlscripts.ml.feature.pca import *
from scipy.stats import mannwhitneyu, ttest_ind
from mlscripts.ml.hebbian_clustering import *

def best_cluster(cluster_mapping, data):
    #calculate distances (maybe better use cosine distances?)
    distances = squareform(pdist(data.todense()))
    #mean over all distances (for comparison)
    global_mean = mean(distances)
    n_cluster = np.max(cluster_mapping) + 1
    #mean, mann-whitney-u-test, t-test for every cluster
    means = np.zeros(n_cluster)
    mannwhitney = np.zeros(n_cluster)
    ttest = np.zeros(n_cluster)
    for i in range(n_cluster):
        #create sub-matrix of items belonging to cluster i
        indices = (i == cluster_mapping)
        subset = distances[indices, :]
        subset = subset[:, indices]
        #divide by the sum of elements without the diagonal (elements are zero)
        means[i] = np.sum(subset)/(len(subset)*len(subset) - len(subset))
        #only use lower diagonal items for tests
        mannwhitney[i] = mannwhitneyu(subset[np.tril_indices(len(subset), -1)], distances[np.tril_indices(len(distances), -1)])[1]
        ttest[i] = ttest_ind(subset[np.tril_indices(len(subset), -1)], distances[np.tril_indices(len(distances), -1)])[1]
    return means, mannwhitney, ttest, global_mean

def json_2_id_text(json):
    entries = []
    ids = []
    for index in range(len(json)):
        entry = json[index]
        entries.append("%s %s %s" % (entry['text_de'], entry['text_en'], entry['text_fr']))
        ids.append(entry['id'])
    return ids, entries

def cluster_entries(entries, n_clusters=5):
    """entries is a list of texts.
    It is assumed that all entries belong to the same project and that only remaining (not yet clustered) entries are included
    None will be returned when no (significant) cluster could be found
    Normally it returns:
      - a dictionary with all the words and their indices
      - the indices of the words considered important
      - a binary list indicating which texts belong to the cluster"""

    vectorizer = TfidfVectorizer(min_df=2, use_idf=True, smooth_idf=True)
    vecs = vectorizer.fit_transform(entries)

    tf_idf_matrix = np.asarray(vecs.todense())
    no_means_data = tf_idf_matrix - np.mean(tf_idf_matrix, 0)

#use library
#(W, W_subgroups) = one_time_learning(no_means_data, n_clusters, 2)
#(x, y, cluster_mapping_2) = project_items(no_means_data, W, W_subgroups)

    #do it by hand to see if results are the same
    (singular_values, cluster_location, eigenvec) = pca(no_means_data, n_clusters)
    #(W, W_subgroups) = one_time_learning(no_means_data, n_clusters, n_visual_dimensions)
    value = np.max(cluster_location, 1)
    cluster_location = np.dot(eigenvec.T, no_means_data.T).T
    #map items to their corresponding cluster
    cluster_mapping = np.argmax(abs(cluster_location), 1)

    #all clusters are highly significant probably. Nevertheless check it
    #mann-whitney-u test has sometimes an error (returns nan) for unknown reasons (a scaling factor becomes negative)
    #therefore use t-test instead
    means, mannwhitney, ttest, global_mean = best_cluster(cluster_mapping, vecs)
    best_cluster_id = np.argsort(means)[0]
    if (ttest[best_cluster_id] > 1E-3):
        #not a significant result. Other clusters could be more significant but this is higly unlikely. So we forget about them
        #return an error
        return None
    """print "global mean: %f" % global_mean
    print "means %s" % str(means)
    print "mean delta %s" % str(global_mean - means)
    print "significance mann-withney-u-test: %s" % str(mannwhitney)
    print "significance t-test: %s" % str(ttest) """

    features = vectorizer.get_feature_names()
    n_words = 20 #number of important words to find

    #find the most important words for every cluster
    important_words = argsort(np.abs(eigenvec.T), 1)[best_cluster_id, -n_words:]
    return features, important_words, (best_cluster_id == cluster_mapping)
    
def classify_entries(entries, classifier_words, strictness=2.0): 
    """Checks which entries belong to the classifier specified by classifier_words and word_dict.
    Returns list of relevance-values of all texts and a boolean list which texts belong to the class"""
    #this is actually not necessary to count all words again, but performance should not be an issue
    word_count_vectorizer = TfidfVectorizer(min_df=2, use_idf=False, smooth_idf=False, norm=None)
    word_counts = word_count_vectorizer.fit_transform(entries)
    word_count_matrix = np.asarray(word_counts.todense())
    relevance = np.sum(word_count_matrix[:, classifier_words], 1)
    relevance[relevance > np.mean(relevance)]
    selected_texts = (relevance > strictness*np.mean(relevance))
    return relevance, selected_texts

json_data=open('C:\\Daten\\atizo\\cti_export.json')    
n_clusters = 5
all_data = json.load(json_data)
data = []
#file contains mutiple projects --> filter all but one project
for index in range(len(all_data)):
    entry = all_data[index]
    if entry['project_id'] == 50:
        data.append(entry)
        """print entry["id"]
        print entry["original_text"]
        print entry["text_de"]"""
json_data.close()

#create two lists: one containing the ids the other one containing the texts
(ids, texts) = json_2_id_text(data)
#for i, text in zip(ids, texts):
    #print i
    #print text
(features, important_words, entries) = cluster_entries(texts, n_clusters)

#print the most important words
print [features[i] for i in important_words]
#the important words and the entries would now be shown to the supervisor

#here should be the words selected from the supervisor
artificial_classifier = ["arbeit", "artist", "artiste", "artistes", "artists", "atelier", "interpretation", u"künstler", "travail", "werk", "work"]

#find the index of the words in the word_dict. In real world the indices should be known already
classifier_index = [features.index(word) for word in artificial_classifier]
(relevance, selected_texts) = classify_entries(texts, classifier_index, 4.0)

#put together the ids and the texts of the selected entries
cluster_texts = [(ids[id], texts[id]) for id, selected in zip(range(len(selected_texts)), selected_texts) if selected == True]
#pprint(data)
