import os

import requests

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm


PEXELS_HEADERS = {
    'Authorization': os.getenv('PEXELS_API_KEY'),
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 Edg/110.0.1587.46'
}

PEXELS_QUERY = ['nature', 'sunset', 'sea']

HITOKOTO_URL = 'https://international.v1.hitokoto.cn/?c=d&c=f&c=h&c=i&c=k&max_length=25'


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


class Quotes(Base):
    __tablename__ = 'quotes'
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    uuid = sqlalchemy.Column(sqlalchemy.String(36))
    hitokoto = sqlalchemy.Column(sqlalchemy.String(100))
    typ = sqlalchemy.Column(sqlalchemy.String(1))
    src = sqlalchemy.Column(sqlalchemy.String(100))
    author = sqlalchemy.Column(sqlalchemy.String(50))
    time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=sqlalchemy.func.current_timestamp())


Base.metadata.create_all(engine, checkfirst=True)
session = sqlalchemy.orm.create_session(bind=engine)


# Fetch Pexels Images
# print(requests.get('https://api.pexels.com/v1/search', headers=PEXELS_HEADERS, params=PEXELS_PARA).json())

images_url = []

for _ in PEXELS_QUERY:
    pexels_search_result = requests.get('https://api.pexels.com/v1/search', headers=PEXELS_HEADERS,
                                        params={'query': _, 'orientation': 'landscape'}).json()
    for _i in pexels_search_result['photos']:
        if session.query(Backgrounds).filter_by(pexels_id=_i['id']).all():
            continue
        print(_)
        new_image = Backgrounds(
            alt=_['alt'],
            avg_color=_['avg_color'],
            pexels_id=_['id'],
            src=_['src']['original'],
            url=_['url']
        )
        session.add(new_image)
        session.commit()
