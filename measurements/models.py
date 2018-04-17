from django.db import models

from activities.models import Activity

<<<<<<< HEAD

=======
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
class Measurement(models.Model):
    activity = models.ForeignKey(Activity, related_name='measurements', on_delete=models.CASCADE)
    type = models.CharField(max_length=16)
    name = models.CharField(max_length=200)
<<<<<<< HEAD
    value = models.CharField(max_length=1024)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '%s:%s' % (self.name, self.value)
=======
    value = models.CharField(max_length=255)
    
    def __str__(self):
        return('%s:%s' % (self.name, self.value))
>>>>>>> b08e6a3e8b2c2dd9bc6e05534b8e9593d0bb7dab
