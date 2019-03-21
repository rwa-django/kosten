from django.db import models
from django.conf import settings
from django.utils import timezone
from vehicles.models import Vehicle_Type

# Vehicle Settings Header
class Vehicle_Setting(models.Model):
    login = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              editable=True)
    type = models.ForeignKey(Vehicle_Type,
                             default=1,
                             on_delete=models.CASCADE)
    info = models.CharField(max_length=200,
                            help_text="Info")
    size_font = models.CharField(max_length=200,
                            help_text="Vorne")
    size_rear = models.CharField(max_length=200,
                            help_text="Hinten")
    booked = models.DateTimeField(default=timezone.now,
                                  editable=False)

    def __str__(self):
        return '{0} {1}'.format(self.login, self.type)

    class Meta:
        unique_together = (('login', 'type', 'info'),)
