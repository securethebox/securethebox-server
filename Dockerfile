FROM python:3.7-slim

COPY . /home/securethebox-server
WORKDIR /home/securethebox-server

# Install Python Requirements
RUN pip3 install virtualenv
RUN python3.7 -m virtualenv venv
ENV PATH="/home/securethebox-server/venv/bin:$PATH"
ENV APPENV="PROD"
RUN . venv/bin/activate
RUN pip3 install -r requirements.txt

# Start securethebox-server service
CMD ./venv/bin/python3.7 app.py