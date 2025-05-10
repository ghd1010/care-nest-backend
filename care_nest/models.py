from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ---- section model -----

class Section(models.Model):
    name = models.CharField(max_length=30)
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return self.name
    
# ---- child model -----

class Child(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    allergies = models.CharField(max_length=50)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child') #parent

    def __str__(self):
        return f'Child: {self.first_name} {self.last_name} : {self.section}'
    
# --------------child achievements model--------------------

TYPES = (
    ('photo', 'Photo'),
    ('badge', 'Badge'),
    ('painting', 'Painting')
)

class ChildAchievements(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    achievement_type = models.CharField(
        max_length = 10,
        choices = TYPES,
        default = TYPES[0][0]
    )
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    image_url = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.title} - {self.achievement_type} for {self.child.first_name}'
    
# ---------- attendance model -----------

STATUS_OPT = (
    ('present', 'Present'),
    ('absent', 'Absent')
)

class Attendance(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    date = models.DateField()
    enter_time = models.TimeField(auto_now=False, auto_now_add=False)
    exit_time = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(
        max_length = 10,
        choices = STATUS_OPT,
        default = STATUS_OPT[0][0]
    )
    def __str__(self):
        return f'{self.child.first_name} {self.child.last_name} - {self.date} : {self.status}'
    
