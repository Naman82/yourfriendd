from django.db import models
from authentication.models import User

# Create your models here.
class Appointment(models.Model):
    doctor = models.ForeignKey(User, related_name="doctor", on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name="patient", on_delete=models.CASCADE)
    date = models.DateTimeField(null=True,blank=True)
    meet_link  = models.URLField(max_length = 500,null=True,blank=True)
    approved = models.BooleanField(default=False)
    conducted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.patient)


class Subscription_Model(models.Model):
    title = models.CharField(max_length = 250)
    description = models.TextField()
    pricing = models.IntegerField()
    expires_in = models.IntegerField()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Subscription Models"
    
class Subscriber(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription_Model, on_delete=models.CASCADE)
    subscribed_on = models.DateField(auto_now_add=True)

class Self_Care(models.Model):
    title = models.CharField(max_length = 500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='selfcare')
    posted_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Self Care Techniques"
    
