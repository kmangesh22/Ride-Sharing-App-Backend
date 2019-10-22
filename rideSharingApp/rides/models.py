from mongoengine import Document,EmbeddedDocument,fields
from users.models import User
# Create your models here.
class RideRequest(Document):
    start = fields.StringField(required=True,null = False)
    destination = fields.StringField(required=True,null = False)
    start_time = fields.StringField(required=True,null = False)
    status = fields.StringField(required=True,null = False)#pending or fullfilled 
    requester_id = fields.ReferenceField(User,required=True,null=False)
    rider_id = fields.ReferenceField(User)




    