FROM python:3 

WORKDIR /usr/src/labs_forum

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000