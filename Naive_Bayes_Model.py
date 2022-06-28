import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from Credentials import TRAINING_DATA_PATH
from nltk.stem.porter import PorterStemmer
import pickle
import os
from nltk.corpus import stopwords
import re

class NaiveBayes:
    def __init__(self, DOCUMENT_PATH):
        try:
            self.reviews = pd.read_csv(DOCUMENT_PATH)
        except UnicodeDecodeError:
            self.reviews = pd.read_excel(DOCUMENT_PATH)
        self.vectoriser = CountVectorizer(max_features = 730)
        self.vectoriser.fit_transform(self.get_corpus(pd.read_csv(TRAINING_DATA_PATH)))
        self.predictions = pd.DataFrame()
        # load model
        with open(os.path.dirname(__file__) + '/' + "trained models/naive_bayes_classifier.pkl", 'rb') as fid:
            self.model = pickle.load(fid)
    
    #Cleans dataset and returns corpus
    def get_corpus(self, dataset):
        ps = PorterStemmer()

        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')

        corpus=[]

        for i in range(len(dataset)):
            review = re.sub('[^a-zA-Z]', ' ', dataset['Reviews'][i])
            review = review.lower()
            review = review.split()
            review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
            review = ' '.join(review)
            corpus.append(review)

        return corpus

    #Returns prediction (1 for positive, 0 for negative)
    def predict(self, reviews):
        if not isinstance(reviews, list):
            reviews = [reviews]
        vectorised_review = self.vectoriser.transform(reviews).toarray()
        prediction = self.model.predict(vectorised_review)
        return prediction

    #Saves predictions as attribute of Naive Bayes object
    def save_predictions(self, predicted_reviews):
        self.predictions = predicted_reviews

    #Returns predictions in a dataframe
    def conduct_CSA(self):
        review_list = self.reviews["Reviews"].tolist()
        predictions = self.predict(review_list)
        predicted_reviews = pd.DataFrame({"Reviews": review_list, "Predictions": predictions})
        self.save_predictions(predicted_reviews)
        return predicted_reviews

    #Returns a dataframe of reviews with no duplicates
    def filter(self):
        bot_removed = self.reviews.drop_duplicates(subset ="Reviews", keep = False, inplace = True)
        return bot_removed

    def compileTopFiveWords(self):
        return {
                "Positive" : 
                    ["Excellent", "Important", "Good", "Helpful", "Useful"], 
                "Negative" : 
                    ["Expensive", "Useless", "Bad", "Terrible", "Disgusting"]
                }