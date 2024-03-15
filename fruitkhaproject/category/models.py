from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="media")
    is_listed = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name
