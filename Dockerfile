FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev

COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY ./app /app
