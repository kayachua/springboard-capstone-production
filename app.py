import tensorflow as tf

from flask import Flask, render_template, request

from transformers import AutoTokenizer, TFAutoModelForSequenceClassification, pipeline
from transformers.utils import logging

#gpus = tf.config.experimental.list_physical_devices('GPU')
#if gpus:
#    try:
#        for gpu in gpus:
#            tf.config.experimental.set_memory_growth(gpu, True)
#        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
#    except RuntimeError as e:
#        print(e)

logging.set_verbosity_error()

tokenizer = AutoTokenizer.from_pretrained("vinai/bertweet-base")

bertweet_stock_tweet = TFAutoModelForSequenceClassification.from_pretrained(
    "./models/bertweet_stock_tweet/",
    num_labels=3,
    id2label={0: 'NEGATIVE', 1: 'NEUTRAL', 2: 'POSITIVE'})

sentiment_eval = pipeline(task='sentiment-analysis', model=bertweet_stock_tweet, tokenizer=tokenizer)

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def index():

    is_result = False
    label = ""
    score = ""

    if request.method == 'POST':
        tweet = request.form['tweet']

        if not tweet:
            flash('Tweet text cannot be empty')
        else:
            is_result = True
            result = sentiment_eval(tweet)
            label = result[0]['label']
            score = result[0]['score']

    return render_template('index.html', is_result=is_result, label=label, score=score)
