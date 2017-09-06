from pyspark import SparkContext
import nltk
import numpy
from math import log
sc= SparkContext('local','pyspark')

from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint

def parseLine(line):
	parts = line.split(',')
	print parts[0]
	label = float(parts[0])
	features = Vectors.dense([float(x) for x in parts[1].split()])
	return LabeledPoint(label, features)


#Train a naive Bayes model.
model = NaiveBayes.train(sc.textFile("train.txt").map(parseLine), 1.0)
test=sc.textFile("test.txt").map(parseLine)
# Make prediction and test accuracy.

#+++++++++++++++++++++++++++++++++++++++++++++++
predictionAndLabel = test.map(lambda p : (model.predict(p.features), p.label))
accuracy = 1.0 * predictionAndLabel.filter(lambda (x, v): x == v).count() / test.count()

print "Accuracy : *****************************"
print accuracy

# Save and load model
#model.save(sc, "myModelPath")
#sameModel = NaiveBayesModel.load(sc, "myModelPath")


#++++++++++++++++++++++++++++++++++++++++++++





































