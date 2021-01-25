from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.models import CourseIntroduction, CourseCurriculum, TeamMember, UserRegistration, UserLogin
from myapp.forms import CourseIntroductionForm, CourseCurriculumForm, TeamMemberForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout


# render is used to display the template when the user requests it.
# get_object_or_404 is used to get the object of a particular model class provided we have the primary key for the same.
# redirect is used to redirect the user to the next page.
# LoginRequiredMixin is used to make sure that the user is logged into the website before he/she accesses certain views.
# and same task is performed by the login_required decorator for the function views.
# REVERSE_LAZY and REVERSE functions are used to apply the url template tagging and use the template tags instead of the
# complete url.
# HttpResponseRedirect is used to redirect the user to some other pages after successfully completing a particular task.

# Create your views here.


# def signup_user(request):
#     if request.method == 'POST':
#         # Getting the values from the signup form.
#         username = request.POST.get('username')
#         email = request.POST.get('useremail')
#         password = request.POST.get('userpassword')
#         confirm_password = request.POST.get('userconfirm_password')
#
#         if password == confirm_password:
#             # Creating an instance of the user credentials using the create class method.
#             user = UserLogin.create(username, email)
#             # This is used to hash the password such that no one can view it.
#             user.set_password(password)
#             # After setting the password we have saved the instance to the database.
#             user.save()
#             return HttpResponseRedirect(reverse('userlogin'))
#         else:
#             return HttpResponseRedirect(reverse('signup'))
#
#     else:
#         return render(request, 'myapp/signup.html')
#
# # Login view will simply take the data from the form and then feed it to the authenticate method which will tell us whether
# # there is an object with the same credentials in the UserLogin database or not. If not he is redirected back to the login
# # page else to the home page of the application.
# def login_user(request):
#     if request.method == "POST":
#         email = request.POST.get('useremail')
#         password = request.POST.get('userpassword')
#         user = UserLogin.authenticate(email=email, password=password)
#         print(user)
#         if user:
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             return HttpResponseRedirect(reverse('userlogin'))
#
#     else:
#         return render(request, 'myapp/userlogin.html')
#

'''This view is for the home page of the site. In the template view we just need to specify the template name which we
want to show to the user or admin.'''
class indexView(TemplateView):
    template_name = 'myapp/index.html'


'''This view is used to display the contents of the team page and all the members of the team. In this view we need to 
pass the template we want to show and the model we want to work on. By default all the objects of the model are passed to
the template which we have specified. We can give whatever name we want to give to the list of all objects in the case
MEMBERS and then use it in templates. The best thing is that we need not to pass it to the templates they are implicitly
passed'''
class teamView(ListView):
    template_name = 'myapp/team.html'
    model = TeamMember
    context_object_name = 'members'


'''This view is used to display all the available courses to the users which have been created by the admin.'''
class coursesView(ListView):
    template_name = 'myapp/course_list.html'
    model = CourseIntroduction
    context_object_name = 'courses'

    # This function is used to sort all the courses in the alphabetic order. The order by is used to do the sorting.
    def get_queryset(self):
        return CourseIntroduction.objects.filter().order_by('course_name')


'''This view contains the details of the particular course the user is interested in like AI, ML etc. In this view we need
not to pass the primary key for the particular course. It implicitly takes the primary key on its on and then we can use
the data with the name of the object we have described in the view. We just need to specify the model name of which the
object is.'''
class courseDetailView(DetailView):
    model = CourseIntroduction
    context_object_name = 'course'
    template_name = 'myapp/course_details.html'


'''This view is used to display the contact us page.'''
class contactView(TemplateView):
    template_name = 'myapp/contact-us.html'


'''This view is used to display the register page. Here the user enter some information to register which is saved in the
user registration model. In this view we have made the form and have not connected to any of the forms class rather taken
the input directly and connected it to the models. For this we have used the request.POST method which is a dictionary and
we have accessed all the inputs given by the user by the means of get method. Then we have created the object of the
model with the help of the create method and not the __init__ method because we do not want to override the __init__
nethod for the super class. After that we just save the model and it is saved in the database.'''
def register(request):
    if request.method == "POST":
        firstname = request.POST["userFirstName"]
        lastname = request.POST["userLastName"]
        address = request.POST.get("userAddress")
        gender = request.POST.get("userGender")
        phonenumber = request.POST.get("userPhoneNumber")
        email = request.POST.get("userEmail")
        rollnumber = request.POST.get("userRollNumber")
        trade = request.POST.get("userTrade")
        college = request.POST.get("userCollege")
        course = request.POST.get("userCourse")

        user = UserRegistration.create(firstname, lastname, address, gender, phonenumber,
                                       email, rollnumber, trade, college, course)
        user.save()
        return redirect('registration_successful', pk=user.pk)

    else:
        return render(request, 'myapp/register.html')


'''This is the page where the user will be redirected after completing the successful registration to review the details
user has filed in.'''
class registration_successful(DetailView):
    template_name = 'myapp/successful_registration.html'
    model = UserRegistration
    context_object_name = 'user'


'''With the help of this view the admin will be able to create the introduction for the courses which will be displayed
in the course list view.'''
class createCourseView(LoginRequiredMixin, CreateView):
    template_name = 'myapp/create_course.html'
    # login_url = '/login/'
    # redirect_field_name = 'myapp/index.html'
    model = CourseIntroduction
    form_class = CourseIntroductionForm


# class updateCourseView(LoginRequiredMixin, UpdateView):
#     # login_url = '/login/'       #This is the URL to which the user will be redirected if he is not authenticated.
#     # redirect_field_name = 'myapp/index.html'    #This is the page where the user will be redirected upon successful login.
#     template_name = 'myapp/create_course.html'
#     form_class = CourseIntroductionForm
#     model = CourseIntroduction


'''With the help of this view we can update the information for the introduction part of any course which is listed
on the course list page. Here we have not used the view class because when we update using the view class the default
redirect page is as mentioned in the get_absolute_url and we do not want to redirect there. Hence we have used the function
view.'''
@login_required
def updateCourse(request, pk):
    obj = get_object_or_404(CourseIntroduction, pk=pk)
    form = CourseIntroductionForm(request.POST or None, instance=obj)   #Here form will work on the given instance and
    # depending on the method if request.post or not values form value will vary. We have passed the instance so that we
    # can use the form to update the data and to show the previously entered data.
    if request.method == "POST":
        if form.is_valid():
            course = form.save()
            if 'course_pic' in request.FILES:
                course.course_pic = request.FILES['course_pic']
                course.save()
            return redirect('courses')
    return render(request, 'myapp/create_course.html', {'form': form})


'''This view enables the admin to delete the course from the course list page. The delete view takes the primary key for
the object to be deleted form the url medium but it is not accepted in the class as argument that functioning is always
implicit. Also we have used the reverse_lazy function because we want the object to be deleted and once it is confirmed
delete we want to move to the new page and not before that.'''
class deleteCourseView(LoginRequiredMixin, DeleteView):
    # login_url = '/login/'
    template_name = 'myapp/Courseintroduction_confirm_delete.html'
    model = CourseIntroduction
    success_url = reverse_lazy('courses')


# class createCourseCurriculumView(LoginRequiredMixin, CreateView):
#     template_name = 'myapp/create_course_curriculum.html'
#     # login_url = '/login/'
#     # redirect_field_name = 'myapp/index.html'
#     model = CourseCurriculum
#     form_class = CourseCurriculumForm


# class deleteCourseCurriculumView(DeleteView):
#     template_name = 'myapp/CourseCurriculum_confirm_delete.html'
#     model = CourseCurriculum
#     success_url = reverse_lazy('courses')


'''This enables the admin to create a new course curriculum section. With this the curriculum should be written only in
sections and not in one go to take the benefits of the styling. We have used the function to create the object for the 
curriculum inorder to redirect the user to the desired page and not to the page we have mentioned in the get_absolute_url.'''
@login_required
def createCourseCurriculum(request, pk):

    course = get_object_or_404(CourseIntroduction, pk=pk)

    if request.method == "POST":
        form = CourseCurriculumForm(request.POST)

        if form.is_valid():
            curriculum = form.save(commit=False)
            curriculum.course_name = course
            curriculum.save()
            return redirect('course_detail', pk=pk)
        else:
            print("The details entered in the curriculum were not valid")

    else:
        form = CourseCurriculumForm()
        return render(request, 'myapp/create_course_curriculum.html', {'form': form})


'''This view helps the admin to update any section of the course curriculum. The update view takes the primary key of the
object as the argument but it does not accept the argument in the class.'''
class updateCourseCurriculumView(LoginRequiredMixin, UpdateView):
    template_name = 'myapp/create_course_curriculum.html'
    model = CourseCurriculum
    form_class = CourseCurriculumForm


'''This view enables the admin to delete any section of the course curriculum from the course detail page. This function
is used to delete the object of the CourseCurriculum class.'''
@login_required
def deleteCourseCurriculum(request, pk):
    curriculum = get_object_or_404(CourseCurriculum, pk=pk) # We have called the object to delete it.
    if request.method == "POST":
        print(curriculum.course_name)
        primary = curriculum.course_name.pk  # Here we are saving the primary key of the course so as to redirect to the
        # detail view of the course afterwards the object is deleted.
        curriculum.delete()
        return redirect('course_detail', pk=primary)
    else:
        context = {}
        context['sub_heading'] = curriculum.sub_heading
        context['pk'] = curriculum.course_name.pk
        return render(request, 'myapp/CourseCurriculum_confirm_delete.html', context)


'''This view enables the admin to add a team member in the page.'''
class createTeamMemberView(LoginRequiredMixin, CreateView):
    template_name = 'myapp/create_team_member.html'
    # login_url = '/login/'
    # redirect_field_name = ''
    model = TeamMember
    form_class = TeamMemberForm


'''This helps the admin to update the information regarding any of the team member displayed on the team.html page.'''
class updateTeamMemberView(UpdateView):
    template_name = 'myapp/create_team_member.html'
    # login_url = '/login/'
    # redirect_field_name = ''
    model = TeamMember
    form_class = TeamMemberForm


'''This view helps to delete the information regarding any of the team member.'''
class deleteTeamMemberView(DeleteView):
    template_name = 'myapp/TeamMember_confirm_delete.html'
    model = TeamMember
    success_url = reverse_lazy('team')
