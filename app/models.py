from django.db import models

# Create your models here.



class img(models.Model):
    icon=models.FileField(upload_to='icon')
    

    
