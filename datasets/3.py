#!/usr/bin/python2
import json
import sys

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.classifier import Classifier 
from naiveBayesClassifier.trainer import Trainer


dataset = [
['Diamond Back Moth','small holes on leaves'],
['Diamond Back Moth','damaged flowers and pods'],
['Diamond Back Moth','deformation of the immature pods'],
['Aphids','deformation of the immature pods'],
['Aphids','yellow leaves'],
['Aphids','curled leaves'],
['Aphids','sticky substance on leaves'],
['Cutworms','plant falls off'],
['Cutworms','plant dies'],
['Cutworms','large caterpillar on soil'],
['Damping-off','no germination'],
['Damping-off','lesions near soil level'],
['Bacterial Soft Rot','offensive odor'],
['Bacterial Soft Rot','watery and slimy on base of the stem']
]
disease_classifier = Trainer(tokenizer)
for data in dataset:
    disease_classifier.train(data[1],  data[0])
disease_classifier = Classifier(disease_classifier.data, tokenizer)
classifications = disease_classifier.classify(sys.argv[1])
classifications_list = []
for classification in classifications:
    classifications_list.append(classification[0])
print json.dumps({'classifications': classifications_list})

