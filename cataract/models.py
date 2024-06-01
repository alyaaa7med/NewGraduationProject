from django.db import models
from accounts.models import User

class CataractDisease(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    retina_image = models.ImageField(upload_to="cataract/images/%Y/%m/%d/%H/%M/%S/")
    result = models.CharField(max_length=30,null =True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)