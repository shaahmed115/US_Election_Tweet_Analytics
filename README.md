#### US_Election_Tweet_Analytics
Sentiment analysis on Tweets related to US Election and classifying them as Pro-Hillary pro-Trump or neutral.

Used Apache Kafka for Live Analysis.

Train the model offline and set up queue between the producer(Tweet Streamer) and the Consumer(Predictor) 

#####Disclaimer:
The work is purely for academic interest and the author in no way supports/endorses the results of the analysis

###Environment:

  1.Python 2.7.9(tweepy,nltk)
  
  2.spark-2.0.0
  
  3.kafka-2.11

###Resources:
  Used the corpus of positive and negative words from 
  
  https://github.com/MKLab-ITI/image-verification-corpus/blob/master/mediaeval2015/src/featureextraction/resources/negative-words.txt
    
  https://github.com/MKLab-ITI/image-verification-corpus/blob/master/mediaeval2015/src/featureextraction/resources/positive-words.txt

Created a list of positive and negative emoticons from Wikipedia(not used yet)  

All features are tagged as 1(pro Trump) 2(pro Hillary).Anti-trump is assumed to imply pro-Hillary

###Features
So far only four features have been extracted and three used:
  PMI-Pointwise Mutual Information(PMI.py)
  
  Absoulte number of positive or negative words
  
  Sum of sentiments of wordvectors for adjective words
  
  Positive or Negative JJR JJS(Comparitive or Superlative) tag between Trump or Hillary (Hillary is deadlier than Trump),not used as matrix is very sparse
 
####Future Work:

  Use Apache Kafka for Live Analysis.Train the model offline and set up queue between the producer(Streamer) and the    Consumer(Predictor) 

####Step 1: Stream Tweets

 1.Run the Streamer.py file in scripts.The tweets get stored in JSON format in mongodb.(Setup the mongo config in the file)
 
 They also get published to a Kafka topic during Live Analysis 
  

####Step2: Feature Extraction(OFFLINE)

  1.Run the Analyzer.py file.It uses map-reduce for optimisation.Check the documentation for submission commands
    
  2.Hand classify the tweets:You can use the script train.py which reads random tweets from the db
   
  3.Align the features into traing and testing files.Run the align_features_testing.py and align_features_training.py to create a files train.txt and test.txt containing features of the form(class,feature1,feature2,feature3)
  

####Step3:Train and save the model,Train the WordVectors  

Run the LogisticRegression(or NaiveBayes) classifier:Run the LogisticRegression.py in scripts/

Run the WordVectorTrainer.py which stores the generated Wordvectors in WordTraining.txt

######Step4
Launch kafka from shell:
		kafka/bin/kafka start-server.sh config/server.properties
Launch Streamer:
		python Streamer.py
Launch Consumer(Also Predictor):
		spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 --master local[8] Predict.py >> output.txt

####Results:
Obtained 67.14 % accuracy for Naive Bayes and 70.2% for LogisticRegression

Format of output stored in output.txt in the form (tweet,location,Sentiment).Sample output:
(u'RT @HuiChenEthics: Another #Trump lie exposed by his own #DOJ; no evidence of wiretapping at Trump Tower. #Resist #Impeach\n\nhttps://t.co/HT\u2026', '', -1)

Most tweets have geodata disabled so the coordinates are empty for most tweets
  
######Future Work:
	Geographic visualisation for sentiment-Plot the coordinates on world map and color code the sentiments in a live fashion
	Improve sentiment analysis.For example:
	"It's only quiet if we let it be quiet. RT now to make @realDonaldTrump answer for his sabotage." is classified as neutral.

