FROM python:3.10.12-bookworm

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
ENV API_KEY API_KEY_VALUE_HERE
 
