import streamlit as st

from transformers import pipeline
# import torch
from moviesapp import MoviesApp
import re
import pandas as pd
import altair as alt

@st.cache(allow_output_mutation = True)
def init_model():
    movieapp = MoviesApp()
    return movieapp

movieapp = init_model()

def highlight_answer(reviews):
    """
    Surrounds the answer given by the QA model with <mark> tags
    so that it is highlighted in the article
    :param text:
    :param predictions:
    :return:
    """
    text = reviews['review_text']
    text = re.sub(movieapp.re_html_tags, "", text)
    prev_start, prev_end = 0, 0
    l_text = []
    for polarity in reviews['polarities']:
        label = polarity['label']
        if label != 'LABEL_2':

            answer = polarity['text']
            start = int(polarity['start'])
            end = int(polarity['end'])
            color_tag = movieapp.mapping_labels_colors[label][0]
            highlighted_text = f'<span style="background-color: {color_tag}">{answer}</span>'

            l_text.append(text[prev_start: start])
            l_text.append(highlighted_text)

            prev_start = end + 1
            # text = re.sub(f"({answer})", r'<span style="background-color: {}">\1</span>'.format(color_tag), text)

    l_text.append(text[prev_start:])
    reviews['review_text'] = " ".join(l_text)
    return reviews

def get_colour_code():
    # writing colour code on main page
    l_colours = []
    for colours in movieapp.mapping_labels_colors.items():
        label, colour_code, colour_meaning = colours[0], colours[1][0], colours[1][1]
        if label != 'LABEL_2':
            l_colours.append(f'<span style="background-color: {colour_code}">{colour_meaning}</span>')
    joined = " ".join(l_colours)
    return f"**Colour code :** {joined}"

def results_to_dataframe(review):
    return pd.DataFrame.from_records(review['polarities'])

def chart_polarity_proportion(df_review):
    """
    Charts using Altair the proportions of each type of polarity in that review
    :param review:
    :return:
    """
    norm = df_review.sentiment.value_counts(normalize=True) * 100

    norm = norm.rename_axis('polarity').reset_index()
    # remove any neutral data that could have been found
    norm = norm[~norm.polarity.isin(['Neutral'])]

    data = {x[0]: x[1] for x in zip(norm.polarity.values, norm.sentiment.values)}
    # data
    sentiment = []
    proportion = []

    for sentiment_type in movieapp.sentiment:
        sentiment.append(sentiment_type)
        if not sentiment_type in data:
            proportion.append(0)
        else:
            proportion.append(data[sentiment_type])

    source = pd.DataFrame({'Sentiment': sentiment,
                           'Proportion': proportion})

    c = alt.Chart(source).mark_bar().encode(
        x='Proportion:Q',
        y = 'Sentiment:N',
        color = alt.Color('Sentiment:N',
                          scale = alt.Scale(
                              domain=movieapp.sentiment,
                              range=movieapp.colours
                          )
                          )
    )
    return c

def global_polarity_bar(review):
    percent = review['global']['score']
    percent = "{:.2f}".format(percent * 100)
    label = review['global']['polarity']
    if label == "Positive":
        colour_code = "#A6F54C"
    else:
        colour_code = "#F53367"
    return f"""<div class="w3-light-grey">
  <div style="height:24px;width:{percent}%;background-color:{colour_code};"></div>
</div>{percent} {label}"""

def get_review():
    """
    Retrieves random document from the database
    :return:
    """
    # review = movieapp.get_review()
    review = movieapp.get_processed_review()
    review = highlight_answer(review)

    return review

def main():
    """
    Loading main application
    :return:
    """

    review = get_review()

    st.write(f"# {review['review_summary']}")
    st.write(f"## {review['review_date']}")

    st.write(review['review_text'], unsafe_allow_html=True)
    st.write(get_colour_code(), unsafe_allow_html=True)

    if review['polarities']:
        df_review = results_to_dataframe(review)
        c = chart_polarity_proportion(df_review)
        st.altair_chart(c, use_container_width=True)

    st.write(global_polarity_bar(review), unsafe_allow_html=True)

    random_review = st.button('Select another review')
    if random_review:
        review = get_review()

if __name__ == "__main__":
    main()