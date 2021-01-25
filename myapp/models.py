from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend

# Create your models here.

# class UserLoginManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         if not username:
#             raise ValueError("Users must have a username")
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    # def create_superuser(self, username, email, password):
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         username=username,
    #         password=password
    #     )
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user


# Once we have created the model for the custom user then we have to register in the settings.py with the name AUTH_USER_LOGIN.
class UserLogin(AbstractBaseUser):

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=20) Password field is present by default and there s no need for us to this.
    # The following fields are the fields which we have to enter by default and have no options for these. Without these
    # are user model will not work.
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    # is active is for whether the user is active or his/her account is blocked.
    is_active = models.BooleanField(default=True)
    # staff is under the super user and has some authorities but not all.
    is_staff = models.BooleanField(default=False)
    # This attribute defines whether the user is by default super user or not.
    is_superuser = models.BooleanField(default=False)

    # This is the field which will be required for login and which will be used to show the entry in the database.
    USERNAME_FIELD = 'email'
    # These are the fields which are required except for the username field because the username field is by default required.
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return self.email

    # This method is to tell whether the user has permission for the particular action which he tends to do.
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    # This method is used to tell whether the user has any permissions w.r.t. the app he is in.
    def has_module_perms(self, app_label):
        return False

    # This method is used to create the object of the model by using the data obtained from the form. The data is fed into
    # the cls method which returns the object for the model and which is further returned to the view.
    @classmethod
    def create(cls, username, email):
        user = cls(username=username,
                   email=email)
        return user

    # This function will help us authenticate the user from the database, basically we take the data from the form and feed
    # it to this function using the view. Now, this function will use get method to get the object for the given email id
    # from the database. If no such objects exist then it returns None. If object exist then we check the passwords using
    # check_password method which matches the input password and the password saved in the database. If the passwords
    # matches then the user is redirected to the home page view else user is redirected back to the login page.
    @classmethod
    def authenticate(cls, email=None, password=None):
        try:
            # Try to find a user matching your username
            user = UserLogin.objects.get(email=email)

            #  Check the password is the reverse of the username
            if check_password(password, user.password):
                # Yes? return the Django user object
                return user
            else:
                # No? return None - triggers default login failed
                return None
        except UserLogin.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None


'''This model keeps the information of the data which will be displayed on the course list page and give the introduction
about any course.'''
class CourseIntroduction(models.Model):

    course_name = models.CharField(max_length=256)
    quotes = models.TextField(max_length=256)
    introduction = models.TextField(max_length=256)
    course_pic = models.ImageField(upload_to="images")

# This function returns the name of the course whenever the object of this class is refered.
    def __str__(self):
        return self.course_name

#This function defines the url where the admin will be directed once he has created or updated the information of any
# instance using the create or the update view only.
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


'''This model is used to store the curriculum of the course in sections and has a foreign key related to the course
introduction which enables us to refer to all the curriculum sections available related to that particular course.'''
class CourseCurriculum(models.Model):

    course_name = models.ForeignKey(CourseIntroduction , on_delete=models.CASCADE, related_name='curriculum')
    sub_heading = models.CharField(max_length=256)
    curriculum = models.TextField(max_length=1500)

    def __str__(self):
        return self.sub_heading

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={"pk": self.course_name.pk})


'''This model stores the data of the team members.'''
class TeamMember(models.Model):

    name = models.CharField(max_length=30)
    course = models.CharField(max_length=30)
    graduation = models.CharField(max_length=30)
    experience = models.TextField(max_length=50)
    photo = models.ImageField(upload_to='member')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team')


'''This model stores the user data which is given by the user during registration.'''
class UserRegistration(models.Model):

    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.TextField()
    gender = models.CharField(max_length=20)
    phone_number = models.PositiveIntegerField()
    email = models.EmailField()
    roll_number = models.PositiveIntegerField()
    trade = models.CharField(max_length=30)
    college = models.CharField(max_length=40)
    course = models.CharField(max_length=20)

    def __str__(self):
        return self.firstname

    def get_absolute_url(self):
        return reverse('index')

# The class method described below is used to create the instance of this class with the values taken from the form.
# When we have a form associated with the model we do not need this method but incase the form is made by us and we want
# to store the data of it in a model then we need to define this method which takes as parameters the values entered in the
# form and since it does not has a __init__ function we use cls() to initialise all the values. Because This class is
# inherinting the models class hence we shall avoid overriding the __init__ method because we want to use the init method
# of the parent class hence we use the create method.
    @classmethod
    def create(cls, firstname, lastname, address, gender, phonenumber, email, rollnumber, trade, college, course):
        user = cls(firstname=firstname,
                   lastname=lastname,
                   address=address,
                   gender=gender,
                   phone_number=phonenumber,
                   email=email,
                   roll_number=rollnumber,
                   trade=trade,
                   college=college,
                   course=course)
        return user


