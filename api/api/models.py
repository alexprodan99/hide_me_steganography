import uuid
from django.db import models

# upload to /media/<uuid>.<extension>
def get_file_path(instance, filename):
    extension = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), extension)
    return filename

class File(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    file = models.FileField(blank=False, null=False, upload_to=get_file_path)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    
    