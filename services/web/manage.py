from project import create_app
import os
import logging
from decouple import config as config_decouple

ENV = 'LOCALHOST'
if config_decouple('PRODUCTION',default=False):
    ENV = 'PROD'

app = create_app(ENV)
if __name__== '__main__':
    if app is not None:
        app.run(host=os.environ.get('HOST'),port=os.environ.get('PORT'))