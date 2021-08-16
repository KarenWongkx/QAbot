FROM python:3.7-slim

WORKDIR /automation_training

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    build-essential \
    software-properties-common \
    nano \
    ca-certificates \
    libjpeg-dev \
    libpng-dev &&\
    rm -rf /var/lib/apt/lists/*

RUN yes | pip install \
    wheel \
    uwsgi \
    flask \
    nltk==3.5 \
    Bani==0.7.2\
    nlpaug==1.1.3 &&\
    pip cache purge

RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

RUN python -m pip install -U watchdog[watchmedo]

COPY faqStore ./faqStore/
COPY generatedModel ./generatedModel/
COPY bot.py bot.ini ./

#CMD watchmedo auto-restart -d ./generatedModel/model_info.txt python3 ./bot.py
CMD watchmedo auto-restart -d ./generatedModel/model_info.txt -- uwsgi --ini ./bot.ini

#CMD ["uwsgi", "bot.ini"]
