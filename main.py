from project import create_app, db
import redis
import os


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))