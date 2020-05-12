from transformers import pipeline
# import spacy
import pymongo
import random
import re

class MoviesApp():

    def __init__(self, spanner_config = None, b_classifier_config = None, m_classifier_config = None):
        # config for pipelines

        # if spanner_config:
        #     self.spanner_config = spanner_config#
        # else:
        #     self.spanner_config = 'models/ner_polarity/'
        #
        # if b_classifier_config:
        #     self.b_classifier_config = b_classifier_config
        # else:
        #     self.b_classifier_config = {'pipeline_type' : 'sentiment-analysis',
        #                 'model_path' : 'models/imdb_classification/model_save/'
        #                 }
        #
        # if m_classifier_config:
        #     self.m_classifier_config = m_classifier_config
        # else:
        #     self.m_classifier_config = {'pipeline_type' : 'sentiment-analysis',
        #                 'model_path' : 'models/treebank_multiclass_84/model_save/'
        #                 }

        self.db = self.connect_mongodb()
        self.reviews_spoilers = self.db.reviews_spoilers
        self.processed_reviews = self.db.processed_reviews
        self.len_collection = self.processed_reviews.count()
        self.all_docs = self.processed_reviews.find({})

        # self.len_collection = self.reviews_spoilers.count()
        # self.all_docs = self.reviews_spoilers.find({})

        # self.m_classifier = self.load_pipeline(self.m_classifier_config)
        # self.b_classifier = self.load_pipeline(self.b_classifier_config)
        # self.spanner = spacy.load(self.spanner_config)

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
        client = pymongo.MongoClient(host="mongodb://localhost:27017")
        db = client.movie_reviews
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
    # def classify_text(self, text):
    #     """
    #     Classify the text either positively or negatively
    #     :param text:
    #     :return:
    #     """
    #     predictions = self.b_classifier(text)[0]
    #     if predictions['label'] == "LABEL_1":
    #         predictions['polarity'] = 'Positive'
    #     else:
    #         predictions['polarity'] = 'Negative'
    #     predictions['score'] = predictions['score'].item()
    #
    #     return predictions
    #
    # def process_text(self, text):
    #     """
    #     Process a given text by finding the portions in the text
    #     that carry a polarity and by classifying them
    #     :param text:
    #     :return:
    #     """
    #     doc = self.spanner(text)
    #     l_polarities = []
    #     for polarity_en in doc.ents:
    #         polarity_text = polarity_en.text
    #         predictions = self.m_classifier(polarity_text)[0]
    #         predicted_label = predictions['label']
    #         if predictions['score'] > .8:
    #             start, end = polarity_en.start_char, polarity_en.end_char
    #             predictions['start'] = start
    #             predictions['end'] = end
    #             predictions['text'] = polarity_text
    #             predictions['score'] = predictions['score'].item()
    #             predictions['sentiment'] = self.mapping_labels_colors[predicted_label][1]
    #             l_polarities.append(predictions)
    #     return l_polarities


    # def process_review(self):
    #     """
    #     Retrieves a random document from the databse
    #     :return:
    #     """
    #     review = self.get_random_document()
    #     review['global'] = self.classify_text(review['review_text'])
    #     review['polarities'] = self.process_text(review['review_text'])
    #     return review
