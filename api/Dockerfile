FROM python:3.10
WORKDIR /var/app
COPY ./app.py /var/app/app.py
COPY ./config.py /var/app/config.py
COPY ./api /var/app/api
COPY ./db /var/app/db
COPY ./models /var/app/models
COPY ./services /var/app/services
COPY ./requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt

