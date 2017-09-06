# US_Election_Tweet_Analytics
Sentiment analysis on Tweets related to US Election and classifying them as Pro-Hillary pro-Trump or neutral

###Environment:

  1.Python 2.7.9(tweepy,nltk) _You may need to use nltk.download() to use stopwords etc_.  
  2.spark-2.0.0

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
  

####Step2: Feature Extraction

Note:I havent used file writing because of a clash in python 2/3 created problems in formatting.So I just redirected the output to the files in resources directory

  1.Run the Analyzer.py file.It uses map-reduce for optimisation.Check the documentation for submission commands
    
  2.Hand classify the tweets:You can use the script train.py which reads random tweets from the db
   
  3.Align the features into traing and testing files.Run the align_features_testing.py and align_features_training.py to create a files train.txt and test.txt containing features of the form(class,feature1,feature2,feature3)
  

####Step3:  
Run the Bayes classifier:Run the NaiveBayes.py in scripts/
Run the LogisticRegression classifier:Run the LogisticRegression.py in scripts/

#########Step4
Load the ML model stored in Step3
Classify the other twees from DB using PySpark Map-Reduce.Check the spark documentation for submission.I ran them on local using 8 cores 
####Results:
Obtained 67.14 % accuracy for Naive_Bayes and 70.2% for LogisticRegression


  
  
