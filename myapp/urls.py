from django.urls import path
from myapp import views


# app_name is required only when the url file is being used by the include function in some other urls.py files.
app_name = 'myapp'

urlpatterns = [
    path('create/introduction/', views.createCourseView.as_view(), name='create'),
    path('update/introduction/<int:pk>/', views.updateCourse, name='update_introduction'),
    path('delete/introduction/<int:pk>/', views.deleteCourseView.as_view(), name='delete_introduction'),
    path('create/<int:pk>/curriculum/', views.createCourseCurriculum, name='curriculum'),
    path('update/curriculum/<int:pk>/', views.updateCourseCurriculumView.as_view(), name='update_curriculum'),
    path('delete/curriculum/<int:pk>/', views.deleteCourseCurriculum, name='delete_curriculum'),
    path('create/member/', views.createTeamMemberView.as_view(), name='create_team_member'),
    path('update/member/<int:pk>', views.updateTeamMemberView.as_view(), name='update_team_member'),
    path('delete/member/<int:pk>', views.deleteTeamMemberView.as_view(), name='delete_team_member')
]