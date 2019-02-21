from django.db import models
from django.conf import settings
from django.utils import timezone

# Vehicle Type
class Vehicle_Type(models.Model):
    login = models.CharField(max_length=200)
    type = models.CharField(max_length=10,
                            default='CAR',
                            help_text="Type")
    pos = models.SmallIntegerField(default=1)
    aktiv = models.BooleanField(default=False,
                                help_text="Aktiv")
    label = models.CharField(max_length=200,
                             help_text="Beschreibung")

    def __str__(self):
        return '{0} - {1}'.format(self.login, self.label)

    class Meta:
        unique_together = (('login', 'type', 'pos'),)
        ordering = ['login', 'pos']           # sortierung mit - dreht die Sortierung

# Vehicle Fuel Header
class Vehicle_Fuel(models.Model):
    login = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              editable=True)
    type = models.ForeignKey(Vehicle_Type,
                             default=1,
                             on_delete=models.CASCADE)
    info = models.CharField(max_length=200,
                            help_text="Info")
    booked = models.DateTimeField(default=timezone.now,
                                  editable=False)

    def __str__(self):
        return '{0} {1}'.format(self.login, self.type)

    class Meta:
        unique_together = (('login', 'type'),)


# Vehicle Fuel Positions
class Vehicle_Fuel_Pos(models.Model):
    fuel_id = models.ForeignKey(Vehicle_Fuel,
                               on_delete=models.CASCADE)
    pos = models.SmallIntegerField(default=1)
    booked = models.DateTimeField(default=timezone.now,
                                  editable=False)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2,
                                 help_text="Kosten")
    km = models.PositiveIntegerField(default=0,
                                     help_text="KM Stand")
    liter = models.DecimalField(default=0,
                                max_digits=10,
                                decimal_places=2,
                                help_text="Liter")
    info = models.CharField(max_length=200,
                            help_text="Buchungs Info")
    average = models.DecimalField(max_digits=10,
                                  default=0,
                                  decimal_places=2,
                                  help_text="Durchschnittsverbrauch")

    def __str__(self):
        return '{0} - {1} / {2}/{3}/{4}'.format(self.pos, self.amount, self.km, self.liter, self.booked)

    class Meta:
        unique_together = (('fuel_id', 'pos'),)
        ordering = ['fuel_id', '-pos']           # sortierung mit - dreht die Sortierung