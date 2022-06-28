# Import everything
import pandas as pd
import os
from transformers import TFDistilBertForSequenceClassification
from transformers import DistilBertTokenizerFast



class Distilbert:
    def __init__(self, DOCUMENT_PATH):
        try:
            self.reviews = pd.read_csv(DOCUMENT_PATH)
        except UnicodeDecodeError:
            self.reviews = pd.read_excel(DOCUMENT_PATH)
        self.model = TFDistilBertForSequenceClassification.from_pretrained(os.path.dirname(__file__) + '/' + "trained models/distilbert_classifier", from_pt=True)
        self.tokeniser = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
        self.predictions = pd.DataFrame()
        self.top_five_words = {}
        self.corpus_predictions = pd.DataFrame()

    # Remove fake bot reviews
    def filter(self):
        filtered_reviews = self.reviews.copy()
        filtered_reviews.drop_duplicates(subset ="Reviews",keep = False, inplace = True)
        return filtered_reviews, self

    

