from mongoengine import Document,EmbeddedDocument,fields
import datetime


class Name(EmbeddedDocument):
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=False)
  


class User(Document):
    name = fields.EmbeddedDocumentField(Name)
    email = fields.EmailField(null = False,required=True)
    password = fields.StringField(null=False,required=True)
    gender = fields.StringField(null = False)
    license_no = fields.StringField(null = False)
    mobile_no = fields.StringField(null=False,max_length=10, required=True)
    token = fields.StringField()
    created_at = fields.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.datetime.utcnow)
