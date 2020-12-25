from app import create_app

from decouple import config as config_decouple

ENV = 'LOCALHOST'
if config_decouple('PRODUCTION',default=False):
    ENV = 'PROD'

app = create_app(ENV)
if __name__== '__main__':
    app.run(host='localhost',port=9000)
