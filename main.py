from project import create_app, db
from rq import Connection, Worker
import os
from dotenv import load_dotenv

LOCAL = bool(os.getenv('LOCAL', 0))
if LOCAL:
    load_dotenv('./config/.env.local')
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))