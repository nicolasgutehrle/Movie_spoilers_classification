from transformers import pipeline
# import spacy
import pymongo
import random
import re
import os

class MoviesApp():

    def __init__(self, ):

        self.db = self.connect_mongodb()
        self.reviews_spoilers = self.db.reviews_spoilers
        self.processed_reviews = self.db.processed_reviews
        self.len_collection = self.processed_reviews.count()
        self.all_docs = self.processed_reviews.find({})

        self.re_html_tags = re.compile(r"(<\\?[^>]*>)")

        self.mapping_labels_colors = {
            'LABEL_0' : ('#e45756', 'Very bad'),
            'LABEL_1': ('#f58518', 'Bad'),
            'LABEL_2': ('#000000', 'Neutral'),
            'LABEL_3': ('#72b7b2', 'Good'),
            'LABEL_4': ('#4c78a8', 'Very good'),
        }
        self.sentiment = ['Very bad', 'Bad', 'Good', 'Very good']
        self.colours = ['#e45756', '#f58518', '#72b7b2', '#4c78a8']

    def connect_mongodb(self):
        """
        Connect to local MongoDB instance
        :return:
        """
        try:
            client = pymongo.MongoClient(os.environ['MONGOLAB_URI'])
            db = client.get_default_database()
        except KeyError:
        # if not os.environ['MONGOLAB_URI']:
            client = pymongo.MongoClient(host="mongodb://localhost:27017")
            db = client.movie_reviews
        # else:
        #     client = pymongo.MongoClient(os.environ['MONGOLAB_URI'])
        #     db = client.get_default_database()
        return db

    def load_pipeline(self, config):
        """
        Initialize an NLP pipeline given a config dictionnary
        with the pipeline type and the model path
        :param config:
        :return:
        """
        nlp = pipeline(config['pipeline_type'],
                       model=config['model_path'],
                       tokenizer=config['model_path'])
        return nlp

    def get_random_document(self):
        """
        Retrieve randomly a document from the database
        :return:
        """
        rand_int = random.randint(0, self.len_collection)
        return self.all_docs[rand_int]

    def get_processed_review(self):
        """
        Retrieve an already processed review from the database
        :return:
        """
        review = self.get_random_document()
        return review

    def get_specific(self, key, value):
        review = self.processed_reviews.find_one({key : value})
        return review
