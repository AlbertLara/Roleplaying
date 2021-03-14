from project import create_app, db
import redis
from flask.cli import FlaskGroup
from rq import Connection, Worker
import os


app = create_app()

cli = FlaskGroup(create_app=create_app)

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

@cli.command('run_app')
def run():
    app.run(host='0.0.0.0', port=os.getenv('PORT'))

if __name__ == "__main__":
    cli()