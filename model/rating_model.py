from mongoengine import connect
from wtforms import ValidationError
from mongoengine import Document, StringField, ListField, URLField,IntField
import validators

# Replace the values with your MongoDB URI and other settings
db_uri = "mongodb+srv://akashh2151:aOSefZ94SgQEkzmg@cluster0.25xmos0.mongodb.net/?retryWrites=true&w=majority"
connect(host=db_uri, db="emc_project2151")

def validate_non_empty(value):
    if isinstance(value, str):
        if not value.strip():
            raise ValidationError("Field cannot be empty.")
    elif isinstance(value, (int, float)):
        # You can customize this part based on your requirements for numeric fields
        pass

def validate_url(value):
    if not validators.url(value):
        raise ValidationError("Invalid URL.")

class RatingInfo(Document):
    rating = IntField(null=False, validation=validate_non_empty, required=True)
    comment = StringField(null=False, validation=validate_non_empty, required=True)
    photos = ListField(URLField(null=False, validation=validate_url, required=True))
