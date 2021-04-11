#!/usr/bin/python2
import json
import sys

from naiveBayesClassifier import tokenizer
from naiveBayesClassifier.classifier import Classifier 
from naiveBayesClassifier.trainer import Trainer


dataset = [
['Aphids','small and soft-bodied pests in colonies located under the leaves'], 
['Aphids','distorted plant parts'],
['Aphids','slow plant growth'],
['Aphids','plant covered with sticky substance'],
['Leaf Miner','winding and whitish tunnels on the surface of the leaves'],
['Cabbage Loopers','green caterpillars with longitudinal white stripes'],
['Cabbage Loopers','holes on leaves'],
['Cutworms','fat caterpillars, basically gray, brown, or black with 41 to 51 mm long when fully grown'],
['Cutworms','damaged stem'],
['Bacterial Leaf Spot','small water-soaked spots on older leaves then quickly turn black'],
['Bacterial Leaf Spot','holes on leaves'],
['Lettuce Drop','older leaves wilt'],
['Lettuce Drop','older leaves collapse'],
['Lettuce Drop','brown crown tissue'],
['Lettuce Drop','holes on leaves'],
['Anthracnose','water-soaked spots that turn yellow'],
['Anthracnose','white to pink spore masses of the fungus in the center of the lesions'],
['Anthracnose','damaged leaf becomes papery'],
['Anthracnose','holes on leaves'],
['Tipburn', 'browing of leaf margins'],
['Tipburn', 'brown veins']
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

