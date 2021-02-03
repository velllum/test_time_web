import uuid

from app import db



class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    limit = db.Column(db.Integer)
    name = db.Column(db.String(100), nullable=True)

    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(*args, **kwargs)

    """Получить имя файла архива"""
    @property
    def get_name_archive(self):
        return uuid.uuid5(uuid.NAMESPACE_DNS, self.url).hex


    def __repr__(self):
        return f'{self.id} | {self.limit} | {self.url}'

# db.create_all()

