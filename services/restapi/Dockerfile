FROM python:3.8

WORKDIR /usr/src/restapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/restapi/requirements.txt
RUN pip install -r requirements.txt

# copy services
COPY . /usr/src/restapi/

CMD [ "flask", "run", "--host=0.0.0.0", "--port=8080" ]