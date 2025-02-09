from django.db import models




class Team(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name