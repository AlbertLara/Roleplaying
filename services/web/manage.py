from project import create_app
import os
import logging
from decouple import config as config_decouple

ENV = os.environ.get('ENV')

app = create_app(ENV)
if __name__== '__main__':
    app.run(host=os.environ.get('HOST'),port=os.environ.get('PORT'))
