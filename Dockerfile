FROM python:3.8

WORKDIR /roleapp

COPY roleapp/run.py /roleapp

RUN mkdir app

COPY roleapp/app /roleapp/app

RUN pip install -r app/requirements.txt

EXPOSE 9000

CMD [ "python", "run.py"]