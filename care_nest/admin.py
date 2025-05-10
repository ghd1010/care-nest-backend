from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Child, 
    ChildAchievements,
    Attendance,
    Section
    )

# Register your models here.

admin.site.register(Child)
admin.site.register(ChildAchievements)
admin.site.register(Attendance)
admin.site.register(Section)



# admin.site.register(Parent)
