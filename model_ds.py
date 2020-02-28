from flask_mongoengine import Document
from apollo_db import db


class DataSource(Document):
    name = db.StringField(max_length=50, unique=True, required=True)
    description = db.StringField(max_length=50)
    meta = {
        'indexes': [
            {'fields': ['+name']}
        ]
    }


if __name__ == "__main__":

    data_source = DataSource(name="PTG", description="python tech group data")
    data_source.save()
