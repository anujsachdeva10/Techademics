from myapp.models import CourseIntroduction, CourseCurriculum, TeamMember, UserRegistration, UserLogin
from django.contrib import admin

# Register your models here.

'''We need to register our models here so that we can view the models in the admin panel. If we do not register the
models then the models will not be shown in the admin panel.'''

admin.site.register(CourseIntroduction)
admin.site.register(CourseCurriculum)
admin.site.register(TeamMember)
admin.site.register(UserRegistration)
admin.site.register(UserLogin)