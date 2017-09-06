from pyspark import SparkContext
import urllib
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from time import time
from pyspark.mllib.regression import LabeledPoint
from numpy import array

sc= SparkContext('local','pyspark') 

data_file = "train.txt"
raw_data = sc.textFile(data_file)

print "Train data size is {}".format(raw_data.count())


test_data_file = "test.txt"
test_raw_data = sc.textFile(test_data_file)

print "Test data size is {}".format(test_raw_data.count())

def parse_interaction(line):
	line_split = line.split(",")
	print line_split[0]
	print array([float(x) for x in line_split[1].split()])
	return LabeledPoint(float(line_split[0]), array([float(x) for x in line_split[1].split()]))

test_data = test_raw_data.map(parse_interaction)
training_data = raw_data.map(parse_interaction)

logit_model = LogisticRegressionWithLBFGS.train(training_data,numClasses=3)
logit_model.save(sc,"model")
labels_and_preds = test_data.map(lambda p: (p.label, logit_model.predict(p.features)))
t0 = time()
test_accuracy = labels_and_preds.filter(lambda (v, p): v == p).count() / float(test_data.count())
tt = time() - t0

print "Prediction made in {} seconds. Test accuracy is {}".format(round(tt,3), round(test_accuracy,4))
