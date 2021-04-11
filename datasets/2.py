#!/usr/bin/python2
import json
import sys

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.classifier import Classifier 
from naiveBayesClassifier.trainer import Trainer


dataset = [
['Damping-off','no emergence of seedling'],
['Damping-off','wilted seedling'],
['Damping-off','lower stem darkens'],
['Bacterial Softrot','leaves turn yellow beginning from the outside toward inside'],
['Bacterial Softrot','plant either die or are dwarfed'],
['Bacterial Softrot','veins within area turns black'],
['Clubroot','wilting during early morning/late night'],
['Flea Beetles','small shiny black beetle/s'],
['Flea Beetles','holes on leaves'],
['Diamondback Moth','holes on leaves'],
['Diamondback Moth','larvae on plant'],
['Aphids','small and soft-bodied pests in colonies located under the leaves'],
['Aphids','distorted plant parts'],
['Aphids','slow plant growth'],
['Aphids','plant covered with sticky substance']
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

