from flask_marshmallow.fields import URLFor

from app import ma
from models import Storage


"""вывод всех данных на гланой странице"""
class AllSchema(ma.Schema):
    class Meta:
        fields = ('id', 'limit', 'url', 'https_url')
        model = Storage
    https_url = URLFor('pagedownloadfile', values=dict(name='<name>', _scheme='http', _external=True))

"""вывод id данных сохраненых в базу"""
class IdSchema(ma.Schema):
    class Meta:
        fields = ('id',)
        model = Storage

"""вывод ссылки для загрузки файла"""
class UrlSchema(ma.Schema):
    class Meta:
        fields = ('https_url',)
    https_url = URLFor('pagedownloadfile', values=dict(name='<name>', _scheme='http', _external=True))

