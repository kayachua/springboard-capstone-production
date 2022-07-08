FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

COPY app.py .
COPY ./templates ./templates
COPY models/bertweet_stock_tweet models/bertweet_stock_tweet

RUN export FLASK_ENV=myenv
RUN export FLASK_APP=app
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "flask", "run", "--host=0.0.0.0"]
