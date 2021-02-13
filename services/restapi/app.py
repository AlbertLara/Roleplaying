from api import create_app
import logging
import os
ENV = os.environ.get('ENV_FILE')
app = create_app(ENV)

if __name__== '__main__':
    app.run(host=os.environ.get('HOST'),port=os.environ.get('PORT'))