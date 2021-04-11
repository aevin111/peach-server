#!/usr/bin/python2
import json
import sys

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.classifier import Classifier 
from naiveBayesClassifier.trainer import Trainer


dataset = [
['Bean Fly','black flies'],
['Bean Fly','damaged lower stem'],
['Bean Fly','plant dies'],
['Aphids','growth stunt'],
['Aphids','yellow leaves'],
['Aphids','curled leaves'],
['Aphids','sticky substance on leaves'],
['Pod Borer','eggs are pale cream laid on young leaves'],
['Pod Borer','pale cream caterpillars ith two rows of dark dots on their backs'],
['Pod Borer','brown moth, wings with white spots'],
['Bruchids','holes on bean'],
['Bruchids','short, cream-colored maggots']
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

