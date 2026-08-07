import os

class Config(object):
    USER=os.environ.get('POSTGRES_USER')
    PASSWORD=os.environ.get('POSTGRES_PASSWORD')
    HOST=os.environ.get('POSTGRES_HOST')
    PORT=os.environ.get('POSTGRES_PORT')
    DB=os.environ.get('POSTGRES_DB')
    SECRET_KEY=os.environ.get('SECRET_KEY')

    SECRET_KEY = os.environ.get("SECRET_KEY")

    PERMANENT_SESSION_LIFETIME = int(os.environ.get('SESSION_LIFETIME_SECONDS', 7200))
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = int(os.environ.get('WTF_CSRF_TIME_LIMIT', 3600))


    SQLALCHEMY_DATABASE_URI =f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATION = False