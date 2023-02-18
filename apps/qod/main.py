import os

import requests

import sqlalchemy
import sqlalchemy.ext.declarative


PEXELS_HEADERS = {
    'Authorization': os.getenv('PEXELS_API_KEY')
}

PEXELS_PARA = {
    'query': 'nature',
    'orientation': 'landscape'
}

PEXELS_QUERY = ['nature', 'sunset', 'sea']


engine = sqlalchemy.engine.create_engine('sqlite:///./apps/qod/db.db?check_same_thread=False', echo=True)
Base = sqlalchemy.ext.declarative.declarative_base()


class Backgrounds(Base):
    __tablename__ = 'backgrounds'
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pexels_id = sqlalchemy.Column(sqlalchemy.Integer)
    url = sqlalchemy.Column(sqlalchemy.String(200))
    avg_color = sqlalchemy.Column(sqlalchemy.String(7))
    src = sqlalchemy.Column(sqlalchemy.String(200))
    alt = sqlalchemy.Column(sqlalchemy.String(200))
    time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=sqlalchemy.func.current_timestamp())


Base.metadata.create_all(engine, checkfirst=True)


# Fetch Pexels Images
# print(requests.get('https://api.pexels.com/v1/search', headers=PEXELS_HEADERS, params=PEXELS_PARA).json())

