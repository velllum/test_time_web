from flask import request, send_from_directory
from flask_restful import Resource

from ClassParse import Parse
from app import db, api, app
from models import Storage
from schemes import AllSchema, IdSchema, UrlSchema
from settings import directory

all_schema = AllSchema(many=True)
id_schema = IdSchema()
url_schema = UrlSchema()


"""главная страница сайта"""
class Index(Resource):
    def get(self):
        return all_schema.dump(Storage.query.all())

    """добавление данных в базу"""
    def post(self):
        data = request.json
        url = Storage(url=data['url'], limit=data['limit'])
        db.session.add(url)
        db.session.commit()
        return id_schema.dump(url)


"""страница парсинга файла"""
class PageParseFile(Resource):
    def get(self, id):
        data = Storage.query.get_or_404(id)
        parse = Parse(data.url, data.limit)

        if not data.get_name_archive in parse.get_names_files or data.name is None:
            parse.run()
            data.name = data.get_name_archive
            db.session.commit()

        return url_schema.dump(data)


"""страница загрузки файла"""
class PageDownloadFile(Resource):
    def get(self, name):
        data = Storage.query.filter_by(name=name).first_or_404()
        return send_from_directory(directory=directory, filename=f"{data.name}.zip")



api.add_resource(Index, '/')
api.add_resource(PageParseFile, '/<int:id>')
api.add_resource(PageDownloadFile, '/download/archive/<string:name>')
