from pyspark import SparkContext,SparkConf
from random import randint
from pyspark.sql import *
import urllib
from pyspark.mllib.classification import LogisticRegressionWithLBFGS,LogisticRegressionModel
import os
from pyspark.mllib.feature import Word2Vec
from time import time
from pyspark.mllib.regression import LabeledPoint
from numpy import array
from classes.PosNeg import PosNegCount
from classes.WordVector import WordVectorAnalyzer
import nltk
import json
from nltk.tree import Tree
import json
from Levenstein import Lev
stop_words = nltk.corpus.stopwords.words('english')
stop_words+=['?','.','!',',']
sparkConf = SparkConf().setMaster("local").setAppName("PredictKafkaTweetStreaming").set("spark.app.id", "Predict")
sc = SparkContext(appName="WordVectorTrainer")
sc.setLogLevel("WARN")
inp = sc.textFile("WordTraining.txt").map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)
WordVectors = {}

for i in model.getVectors().keys():
    WordVectors[i] = model.findSynonyms(i,7)

with open('WordVectors.json', 'w') as fp:
    json.dump(WordVectors, fp)

