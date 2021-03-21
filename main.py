from project import create_app, db
import redis
import json
from flask.cli import FlaskGroup
from rq import Connection, Worker
import click
import os
from dotenv import load_dotenv

LOCAL = bool(os.getenv('LOCAL'))
if LOCAL:
    load_dotenv('./config/.env.local')
app = create_app()

cli = FlaskGroup(create_app=create_app)

@cli.command('create_user')
@click.option('--inputfile')
def create(inputfile):
    file = open(inputfile, encoding='utf-8')
    data = json.load(file)
    file.close()
    from project.utils.models import User
    for row in data:
        name = row['name']
        email = row['email']
        if User.find_user(name, email) is None:
            user = User(email=email,
                        password=row['pwd'],
                        username=name,
                        confirmed=True,
                        active=True)
            user.save_to_db()

@cli.command('create_db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('drop_db')
def drop_db():
    """Drops the db tables."""
    db.drop_all()

@cli.command('run_worker')
def run_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(app.config['QUEUES'])
        worker.work()

if __name__ == "__main__":
    cli()