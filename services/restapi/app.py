from api import create_app
import logging
import os

app = create_app("LOCALHOST_REST")

if __name__== '__main__':

    app.run(host=os.environ.get('HOST'),port=os.environ.get('PORT'))