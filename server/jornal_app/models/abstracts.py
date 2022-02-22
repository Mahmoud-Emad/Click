from django.db import models



def save_media_file_path(self, filename):
    """Handel post media files"""
    allowed_extensions=(
        ['JPEG','JPG','PNG','GIF','TIFF','PSD','PDF','EPS','AI','INDD','RAW'], # For Images
        ['MOV','AVI','MP4','WEBM','MKV'] # For Videos
    )
    file_exe = filename.split('.')[-1]
    if file_exe.upper() in allowed_extensions[0]:
        return f'server/media/posts/images/{self.id}/{self.modified}.{file_exe.lower()}'
    elif file_exe.upper() in allowed_extensions[1]:
        return f'server/media/posts/videos/{self.id}/{self.modified}.{file_exe.lower()}'
    else:
        from django.core.exceptions import ValidationError
        raise ValidationError(
            " Unsupported file extension"
            )   

class TimeStampedModel(models.Model):
    """
    database model for created at and updated at fields
    """
    created  = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PostAbc(TimeStampedModel):
    """
    database model for more fields better than dublecate it
    """
    iframe  = models.CharField(max_length = 500, null = True, blank = True)
    media   = models.FileField(upload_to=save_media_file_path,null = True, blank = True)

    class Meta:
        abstract = True
