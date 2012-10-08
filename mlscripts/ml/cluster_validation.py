#!/usr/local/bin/python
# coding: UTF-8

# released under bsd licence
# see LICENCE file or http://www.opensource.org/licenses/bsd-license.php for details
# Institute of Applied Simulation (ZHAW)
# Author Thomas Niederberger

import numpy as np
import codecs
from decimal import *
import logging

def jaccard_index(list_a, list_b):
    set_a = set(list_a)
    set_b = set(list_b)
    un = set_a.union(set_b)
    inter = set_a.intersection(set_b)
    return 1.0 * len(inter) / (len(un))

def intersection_index(list_a, list_b):
    set_a = set(list_a)
    set_b = set(list_b)
    un = set_a.intersection(set_b)
    return len(un)

def confusion_matrix(groups_a, groups_b, distance=jaccard_index):
    matrix = np.zeros((len(groups_a), len(groups_b)))
    #symmetry not used => performance could be improved
    for i, vec_a in enumerate(groups_a):
        for j, vec_b in enumerate(groups_b):
            jaccard = distance(vec_a, vec_b)
            matrix[i, j] = jaccard
            #matrix[j, i] = jaccard
    return matrix

def precision(prediction, correct):
    set_prediction = set(prediction)
    set_correct = set(correct)
    inter = set_prediction.intersection(set_correct)
    return 1.0 * len(inter) / (len(prediction))

def recall(prediction, correct):
    set_prediction = set(prediction)
    set_correct = set(correct)
    inter = set_prediction.intersection(set_correct)
    return 1.0 * len(inter) / (len(correct))

if __name__ == "__main__":
    logging.basicConfig()

    reference_cluster = [[12032, 12045, 12079, 12121, 12131, 12157, 12333, 12372, 12421, 12422, 12460, 12461, 12657, 12713, 12851, 13010, 13082, 13115, 13207, 13303, 13310, 13684, 13703, 13892, 13896, 13897, 13916, 13933, 13940, 13948, 14032, 12007, 12037, 12087, 12093, 12136, 12237, 12309, 12386, 12390, 12425, 12426, 12431, 12433, 12755, 12814, 12847, 13140, 13312, 13932, 13946, 13949, 14027, 12009, 12053, 12059, 12060, 12069, 12070, 12071, 12104, 12105, 12106, 12112, 12129, 12132, 12141, 12142, 12445, 13144, 13778, 13830, 13947, 14046, 14049, 12144, 12809, 12839, 13681, 13891, 13898, 12030, 12055, 12123, 12156, 12424, 12514, 12996, 13803, 12098, 12147, 12149, 12423, 13469, 14025, 14044, 12011, 13138, 13495, 13972, 13991, 14031, 12040, 12291, 12292, 13081, 13400, 13595, 12012, 12036, 12046, 12047, 12051, 12057, 12115, 14018, 12148, 12288, 12391, 13325, 13496, 14034],
                     [12062, 12066, 12086, 12102, 12103, 12140, 12201, 12451, 13049, 13061, 13381, 13711, 13965, 14014, 12020, 12056, 12065, 12312, 13056, 13265, 13379, 12153, 13535, 13564, 13686, 13880, 14015, 12028, 12058, 12081, 12270, 12021, 12038, 12085, 12116, 12197, 12412, 12788, 12790, 13178, 13185, 13692, 13964],
                     [12013, 12042, 12044, 12076, 12080, 12235, 12254, 12278, 12714, 12817, 13142, 13374, 13667, 13968, 12022, 12031, 12032, 12063, 12150, 12216, 12268, 12545, 12578, 12789, 13143, 13340, 12049, 12196, 12355, 12443, 13683, 12041, 12242, 12324, 12579, 13161, 13906, 12019, 12100, 12497, 12834, 13437, 13687, 13805, 13899, 13945, 13953, 13971, 14028, 14047, 14048],
                     [12015, 12026, 12029, 12088, 12134, 12243, 12275, 12547, 12649, 12712, 13042, 13044, 13210, 13534, 12006, 12010, 12035, 12039, 12050, 12061, 12072, 12073, 12139, 12403, 12413, 12495, 12644, 12757, 12945, 13041, 13050, 13198, 13309, 13345, 13411, 13664, 13689, 13829, 14019, 14020, 14030, 14033, 12008, 12074, 12113, 12384, 12448, 13978, 12091, 12787, 13048, 13286, 13317, 13388, 13602, 13893, 14024, 12043, 12447, 12850, 13147, 13662, 12064, 12092, 12122],
                     [12380, 12551, 12785, 12786, 12794, 12849, 13311, 13316, 13401, 13529, 13530, 12005, 12101, 12114, 12133, 12558, 12750, 13096]]

    reference_sub_cluster = [[12032, 12045, 12079, 12121, 12131, 12157, 12333, 12372, 12421, 12422, 12460, 12461, 12657, 12713, 12851, 13010, 13082, 13115, 13207, 13303, 13310, 13684, 13703, 13892, 13896, 13897, 13916, 13933, 13940, 13948, 14032],
        [12007, 12037, 12087, 12093, 12136, 12237, 12309, 12386, 12390, 12425, 12426, 12431, 12433, 12755, 12814, 12847, 13140, 13312, 13932, 13946, 13949, 14027],
        [12009, 12053, 12059, 12060, 12069, 12070, 12071, 12104, 12105, 12106, 12112, 12129, 12132, 12141, 12142, 12445, 13144, 13778, 13830, 13947, 14046, 14049],
        [12144, 12809, 12839, 13681, 13891, 13898],
        [12030, 12055, 12123, 12156, 12424, 12514, 12996, 13803],
        [12098, 12147, 12149, 12423, 13469, 14025, 14044],
        [12011, 13138, 13495, 13972, 13991, 14031],
        [12040, 12291, 12292, 13081, 13400, 13595],
        [12012, 12036, 12046, 12047, 12051, 12057, 12115, 14018],
        [12148, 12288, 12391, 13325, 13496, 14034],
        [12062, 12066, 12086, 12102, 12103, 12140, 12201, 12451, 13049, 13061, 13381, 13711, 13965, 14014],
        [12020, 12056, 12065, 12312, 13056, 13265, 13379],
        [12153, 13535, 13564, 13686, 13880, 14015],
        [12028, 12058, 12081, 12270],
        [12021, 12038, 12085, 12116, 12197, 12412, 12788, 12790, 13178, 13185, 13692, 13964],
        [12013, 12042, 12044, 12076, 12080, 12235, 12254, 12278, 12714, 12817, 13142, 13374, 13667, 13968],
        [12022, 12031, 12032, 12063, 12150, 12216, 12268, 12545, 12578, 12789, 13143, 13340],
        [12049, 12196, 12355, 12443, 13683],
        [12041, 12242, 12324, 12579, 13161, 13906],
        [12019, 12100, 12497, 12834, 13437, 13687, 13805, 13899, 13945, 13953, 13971, 14028, 14047, 14048],
        [12015, 12026, 12029, 12088, 12134, 12243, 12275, 12547, 12649, 12712, 13042, 13044, 13210, 13534],
        [12006, 12010, 12035, 12039, 12050, 12061, 12072, 12073, 12139, 12403, 12413, 12495, 12644, 12757, 12945, 13041, 13050, 13198, 13309, 13345, 13411, 13664, 13689, 13829, 14019, 14020, 14030, 14033],
        [12008, 12074, 12113, 12384, 12448, 13978],
        [12091, 12787, 13048, 13286, 13317, 13388, 13602, 13893, 14024],
        [12043, 12447, 12850, 13147, 13662],
        [12064, 12092, 12122],
        [12380, 12551, 12785, 12786, 12794, 12849, 13311, 13316, 13401, 13529, 13530],
        [12005, 12101, 12114, 12133, 12558, 12750, 13096]]

    id_file = 'C:\\Daten\\atizo\\desc-file-pro-64.csv'
    #documents = codecs.open(id_file, "r", "utf-8" ).readlines()
    #distance_file = np.genfromtxt(id_file, delimiter=';')
    documents = open(id_file, 'r').readlines()
    ids = []
    ids_text = {}
    for line in documents:
        (id, sep, text) = line.partition(';')
        ids_text[int(id)] = text
        ids.append(int(id))
    ids = np.array(ids)
    #distance_file = np.genfromtxt(id_file, delimiter=' ')

    input_file = 'C:\\Daten\\java-workspace\\Mahout\\topics.txt'
    cluster_file = 'C:\\Daten\\atizo\\cluster-file-pro-64.txt'
    output_file = open(cluster_file, 'w')

    probabilities = np.genfromtxt(input_file, delimiter=',')
    indices = np.argmax(probabilities, 1)
    cluster = []
    for i in range(5):
        values = ids[indices == i]
        print str(i) + '/' + str(len(values)) + ': ' + str(values)
        cluster.append(values)
        output_file.write(str(i) + '\n')
        for key in values:
            output_file.write(ids_text[key])
        output_file.flush()

    conf_jaccard = confusion_matrix(cluster, reference_cluster)
    conf_recall = confusion_matrix(cluster, reference_cluster, recall)
    conf_precision = confusion_matrix(cluster, reference_cluster, precision)
    #confusion = confusion_matrix(cluster, reference_sub_cluster)

    imshow(conf_jaccard, cmap=cm.gray, interpolation="nearest", vmin=0.0, vmax=1.0)#, vmin=0.0, vmax=256.0*256.0)
    figure()
    imshow(conf_recall, cmap=cm.gray, interpolation="nearest", vmin=0.0, vmax=1.0)#, vmin=0.0, vmax=256.0*256.0)
    figure()
    imshow(conf_precision, cmap=cm.gray, interpolation="nearest", vmin=0.0, vmax=1.0)#, vmin=0.0, vmax=256.0*256.0)
    show()
    output_file.flush()
    output_file.close()
