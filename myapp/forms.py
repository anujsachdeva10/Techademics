from django import forms
from myapp.models import CourseIntroduction, CourseCurriculum, TeamMember
from django.contrib.auth.models import User


'''This form is associated with the CourseIntroduction model which is used to display the course list in the website.'''
class CourseIntroductionForm(forms.ModelForm):
    class Meta():
        model = CourseIntroduction
        fields = ('course_name', 'introduction', 'quotes', 'course_pic') #here we need to specify that what fields we want
        # the admin to fill in the form. The rest will not be displayed to the admin.

        # with the help of this widget we can add classes to the fields and customize the form a bit.
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'name_input'}),
            'introduction': forms.Textarea(attrs={'class': 'introduction_input'}),
            'quotes': forms.Textarea(attrs={'class': 'quotes_input'})
        }


'''This form is associated with the CourseCurriculum model and here the admin will enter the details for each section
of the curriculum.'''
class CourseCurriculumForm(forms.ModelForm):
    class Meta():
        model = CourseCurriculum
        fields = ('sub_heading', 'curriculum')

        widgets = {
            'sub_heading': forms.TextInput(attrs={'class': 'sub_heading_input'}),
            'curriculum': forms.Textarea(attrs={'class': 'curriculum_input'})
        }


'''This form is associated with the TeamMember model and here the admin will enter the details for each member of the 
team.'''
class TeamMemberForm(forms.ModelForm):
    class Meta():
        fields = ('name', 'course', 'graduation', 'experience', 'photo')
        model = TeamMember

        widgets = {
            'experience': forms.Textarea(attrs={'class': 'exprience_input'})
        }


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

