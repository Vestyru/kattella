import os

class Config(object):
    USER=os.environ.get('POSTGRES_USER')
    PASSWORD=os.environ.get('POSTGRES_PASSWORD')
    HOST=os.environ.get('POSTGRES_HOST')
    PORT=os.environ.get('POSTGRES_PORT')
    DB=os.environ.get('POSTGRES_DB')
    SECRET_KEY=os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI =f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY =f'{SECRET_KEY}'
    SQLALCHEMY_TRACK_MODIFICATION = True