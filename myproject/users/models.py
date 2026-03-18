from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError


# Create your models here
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Safely open the image; skip resizing if the file is missing
        # or not a valid image (e.g. corrupted default.jpg).
        try:
            img = Image.open(self.image.path)
        except (UnidentifiedImageError, FileNotFoundError, OSError):
            # Do not break user creation just because the default image
            # is invalid or missing.
            return


        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

   