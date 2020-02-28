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

class VersionId(db.EmbeddedDocument):
    ptg_obj_id = db.StringField(required=True, Unique=True, primary_key=True)
    _version = db.IntField(default=1, required=True)

class PTGObject(db.DynamicDocument):
    obj_id = db.StringField(required=True, Unique=True, primary_key=True)
    _version = db.IntField(default=1, required=True)
    creation_time = db.DateTimeField(default=datetime.now, required=True)
    modification_time = db.DateTimeField()

    meta = {
        'collection': "ptg_obj",
        'indexes': [
             ('announce_date', '-announce_date__display_value')
        ]
    }

    def to_json(self):
        data = self.to_mongo()
        return data

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.with_id(id)

    @db.queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-date')

    def shadow_save(self, *args, **kwargs):
        original_collection = self._get_collection_name()
        shadow_collection = '.'.join([original_collection, 'shadow'])

        model_2 = deepcopy(self)
        vid = VersionId(obj_id=self.obj_id, _version=self._version)
        model_2.id = vid
        kwargs['is_shadow'] = True
        model_2.switch_collection(shadow_collection)
        return model_2.save(*args, **kwargs)

    def save(self, *args, **kwargs):
        pprint.pprint(self.to_json())

        # always write all fields
        for f in self._fields.keys():
            self._mark_as_changed(f)

        if kwargs.get('is_shadow', False) or kwargs.get('is_existing', False):
            # Save it
            print('dont reshadow - just save')
            return super(PTGObject, self).save(*args, **kwargs)

        existing_model = PTGObject.objects(__raw__={'_id': {'_id': self.id, '_version': self._version}}).first()
        if existing_model:
            print('existing model - shadow and update')
            self.shadow_save(*args, **kwargs)
            self.modified = datetime.datetime.now()
            inc_version = self._version + 1
            self._version = inc_version
            self.id._version = inc_version
            kwargs['is_existing'] = True
            self.save(*args, **kwargs)
            existing_model.delete()  # updated version is saved, delete old version
        else:
            return super(PTGObject, self).save(*args, **kwargs)
if __name__ == "__main__":

    data_source = DataSource(name="PTG", description="python tech group data")
    data_source.save()
