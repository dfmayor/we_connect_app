import uuid
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission
from django.core.mail import send_mail
from django.db import models
from .manager import UserAccountManager


#class UserPermission(Permission):
    #class Meta:
        #app_label = 'users'
        #permissions =[('do_all', 'Can do all'), ('add_users', 'Can add users'), ('edit_table', 'Can edit table')]


# Create your models here.
User = settings.AUTH_USER_MODEL


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name="Email")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    username = models.CharField(max_length=50, verbose_name='Username', null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserAccountManager()

    class Meta:
        ordering = ('date_joined',)
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.last_name} {self.first_name}'

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_user_permissions(self, obj=None):
        """
            Return a list of permission strings that this user has.
        """
        if not self.is_active or self.is_anonymous:
            return set()

        # Retrieve user permissions from groups
        permissions = self.get_group_permissions(obj)

        # Retrieve user-specific permissions
        user_permissions = [perm.codename for perm in self.user_permissions.all()]

        # Combine and return the permissions
        permissions.update(user_permissions)
        return permissions

    def get_all_permissions(self, obj=None):
        return self.get_user_permissions(obj)


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    course = models.CharField(max_length=255, verbose_name='Course Of Study')
    graduation_year = models.DateField()

    def __str__(self):
        return f'Education for {self.user.email}'


class UserProfile(models.Model):
    Gender = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    Marital_Status = [
        ("Single", "Single"),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widow', 'Widow'),
        ('Others', 'Others')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    i_am_a = models.CharField(max_length=50, verbose_name="I Am A")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)
    bio = models.CharField(max_length=450, verbose_name="Biography")
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number')
    gender = models.CharField(choices=Gender, max_length=10)
    profile_pics = models.ImageField(upload_to='profile_pics', default='img/default_pic.png')
    highest_education = models.ManyToManyField(Education, verbose_name='Education Qualification')
    occupation = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f'Profile for {self.user.first_name} {self.user.last_name}'
