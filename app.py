from flask import Flask
from flask_restx import Api, apidoc
from api.apiAuto import blueprint as blueprintAutho

def main():
    app = Flask(__name__)
    app.register_blueprint(blueprintAutho)
    app.run(debug=True, host='localhost',port=9000)

if __name__ == '__main__':
    main()