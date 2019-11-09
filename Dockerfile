FROM python:3.7-slim

COPY . /home/securethebox-server
WORKDIR /home/securethebox-server

# Install Python Requirements
RUN pip3 install virtualenv
RUN python3.7 -m virtualenv venv
ENV PATH="/home/securethebox-server/venv/bin:$PATH"
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

# Start securethebox-server service
RUN ./venv/bin/python3.7 app.py