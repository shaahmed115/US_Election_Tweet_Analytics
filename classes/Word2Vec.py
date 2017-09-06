from pyspark.mllib.feature import Word2Vec
from pyspark import SparkContext, SparkConf
import nltk
import os
stop_words = nltk.corpus.stopwords.words('english')
stop_words+=['?','.','!',',']

sparkConf = SparkConf().setMaster("local").setAppName("Word2Vec").set("spark.app.id", "Word2Vec")
sc = SparkContext(conf=sparkConf)
#inp = sc.textFile("Trump.txt").map(lambda row: row.split(" "))
tweets=open(os.getcwd() + "/Trump.txt").read.splitlines()
documentDF = sc.createDataFrame(tweets)
word2vec = Word2Vec()
model = word2vec.fit(inp)
result = model.transform(inp)
for row in result.collect():
	text, vector = row
	print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))
