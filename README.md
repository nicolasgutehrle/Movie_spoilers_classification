# Movie Spoilers Sentiment Analysis

This repo is an attempt at using Hugging Face's text classification pipeline. I classifies a review from the Movie Spoilers dataset as either positive or negative.

I followed Chris McCormick tutorial to train a sentiment analysis classifier was trained on the iMDB Dataset. The model used a pre-trained BERT model and reached 89% of accuracy, without tweaking hyper parameters.

However, classical sentiment analysis models work on the text as a whole. I wanted to try to find what element in the text were positive or negative precisely. The only work I could find on fine-grained sentiment analysis was Stanford's Treebank. So I used this dataset to train a NER model spacy that would detect phrases that carry a polarity, from very bad to very positive. The results aren't exceptional (40% precision) and this is probably not the best methodology for such task, but I've wanted to experiment with NER model for a long time.

