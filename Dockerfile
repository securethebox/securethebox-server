FROM python:3.7-buster

COPY . /home/securethebox-server
WORKDIR /home/securethebox-server

# Install Python Requirements
RUN apt-get update -y && apt-get upgrade -y
RUN python3.7 -m virtualenv venv
ENV PATH="./venv/bin:$PATH"
ENV APPENV="PROD"

RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

# Start securethebox-server service
CMD ./venv/bin/python3.7 app.py