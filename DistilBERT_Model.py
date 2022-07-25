# Import everything
import pandas as pd
import os
from transformers import TFDistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast
import tensorflow as tf
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.probability import FreqDist



class Distilbert:
    def __init__(self, url, category):
        try:
            self.reviews = pd.read_csv(url)
        except Exception as e:
            print(e)
            self.reviews = pd.read_excel(url)
        #self.model = TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "trained models/distilbert_classifier/general/3_epoch", from_pt=True)
        if category == "general":
            print("Loading model for general category...")
            self.model = TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "../" + "trained models/distilbert_classifier/general/3_epoch", from_pt=True)
            self.category = category
        elif category == "books":
            print("Loading model for books category...")
            self.model = TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "../" + "trained models/distilbert_classifier/books/8_epoch", from_pt=True)
            self.category = category
        elif category == "electronics":
            print("Loading model for electronics category...")
            self.model =  TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "../" + "trained models/distilbert_classifier/electronics/8_epoch", from_pt=True)
            self.category = category
        elif category == "food":
            print("Loading model for food category...")
            self.model =  TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "../" + "trained models/distilbert_classifier/food/8_epoch", from_pt=True)
            self.category = category
        else:
            print("No suitable category available!")
            self.model = None
            self.category = None
        self.tokeniser = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self.predictions = pd.DataFrame()
        self.top_five_words = {}
        self.corpus_predictions = pd.DataFrame()

    # Remove fake bot reviews
    def filter(self):
        filtered_reviews = self.reviews.copy()
        filtered_reviews.drop_duplicates(subset ="Reviews",keep = False, inplace = True)
        return filtered_reviews, self

    # Data cleaning
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

    # Returns prediction
    # Takes in review as a string of a sentence
    def predict(self, review):
        predict_input = self.tokeniser.encode(review,
                                        truncation=True,
                                        padding=True,
                                        return_tensors="tf")

        tf_output = self.model.predict(predict_input)[0]
        tf_prediction = tf.nn.softmax(tf_output, axis=1)
        labels = ['Negative','Positive']
        label = tf.argmax(tf_prediction, axis=1)
        label = label.numpy()
        prediction = labels[label[0]]
        print(f"Review: {review} , Prediction: {prediction}")
        return prediction

    # Saves predictions as attribute of Naive Bayes object
    def save_predictions(self, predicted_reviews):
        self.predictions = predicted_reviews

    # Check if predictions are done 
    def has_predicted(self):
        return len(self.predictions) != 0

    # Get predicted reviews
    def get_predicted_reviews(self):
        return self.predictions.copy()

    # Conduct sentiment analysis on reviews passed in to initialise model object
    def conduct_CSA(self):
        if self.has_predicted():
            return self.get_predicted_reviews(), self
        else:
            corpus = self.get_corpus(self.reviews.copy())
            predictions = []
            for review in corpus:
                predictions.append(self.predict(review))
            predicted_reviews = pd.DataFrame({"Reviews": self.reviews["Reviews"].copy(), "Predictions": predictions})
            self.corpus_predictions = pd.DataFrame({"Reviews": corpus, "Predictions": predictions})
            self.save_predictions(predicted_reviews)
            return predicted_reviews, self

    # Sort predicted reviews
    def sort_predicted_reviews(self, predicted_reviews):
        good_reviews = predicted_reviews[predicted_reviews["Predictions"] == "Positive"]
        bad_reviews = predicted_reviews[predicted_reviews["Predictions"] == "Negative"]
        return good_reviews, bad_reviews
    
    # Compile top five words of predicted reviews
    def compile_top_five_words(self):
        if len(self.top_five_words) == 0 :
            if not self.has_predicted():
                self.conduct_CSA()
            good_reviews, bad_reviews = self.sort_predicted_reviews(self.corpus_predictions.copy())
            
            # Combine all reviews into a single list and split into indiv words
            good_reviews = good_reviews["Reviews"].str.cat(sep=' ')
            good_reviews = good_reviews.split()
            bad_reviews = bad_reviews["Reviews"].str.cat(sep=' ')
            bad_reviews = bad_reviews.split()

            good_reviews_dist = FreqDist(good_reviews)
            bad_reviews_dist = FreqDist(bad_reviews)
            five_good_words = good_reviews_dist.most_common(5)
            five_bad_words = bad_reviews_dist.most_common(5)

            good_bad_dict = {}
            for word_dist in five_good_words:
                if "Positive" not in good_bad_dict.keys():
                    good_bad_dict["Positive"] = [word_dist[0]]
                else:
                    good_bad_dict["Positive"].append(word_dist[0])

            for word_dist in five_bad_words:
                if "Negative" not in good_bad_dict.keys():
                    good_bad_dict["Negative"] = [word_dist[0]]
                else:
                    good_bad_dict["Negative"].append(word_dist[0])

            self.top_five_words = good_bad_dict
            return good_bad_dict, self
        else:
            return self.top_five_words, self