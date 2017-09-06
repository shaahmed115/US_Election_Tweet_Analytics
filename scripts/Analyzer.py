from pyspark.mllib.feature import Word2Vec
from pyspark import SparkContext, SparkConf
import nltk
import os
from classes.WordVector import WordVectorAnalyzer
from classes.PosNeg import PosNegCount

stop_words = nltk.corpus.stopwords.words('english')
stop_words+=['?','.','!',',']

sparkConf = SparkConf().setMaster("local").setAppName("Word2Vec").set("spark.app.id", "Word2Vec")
sc = SparkContext(conf=sparkConf)
inp = sc.textFile("WordTraining.txt").map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)
WordVectors = {}

for i in model.getVectors().keys():
	WordVectors[i] = model.findSynonyms(i,7)

Positive = open(os.getcwd() + "/positive.txt").read().splitlines()
Negative = open(os.getcwd() + "/negative.txt").read().splitlines()

def Analyze(sentence):
	Analyzer = WordVectorAnalyzer(stop_words,WordVectors,Positive,Negative)
	return Analyzer.FindTweetSentiment(sentence)

parallelised_tweets = sc.textFile("testing_samples.txt")

feat1 = parallelised_tweets.map(lambda sentence:Analyze(sentence.encode('utf-8'))).collect()

f = open('Feat1_test.txt', 'w') 
for token in feat1:
	f.write(str(token) + '\n')
feat2 = parallelised_tweets.map(lambda l : PosNegCount(Positive,Negative).Sentiment(l)).collect()

f = open('Feat2_test.txt', 'w') 
for token in feat2:
	f.write(str(token) + '\n')

			
