from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

# Create your models here.
from django.utils.translation import gettext_lazy

phone_regex = RegexValidator(regex=r"^\+?(88)01[3-9][0-9]{8}$",
                             message=gettext_lazy('Enter Bangladeshi Number with country code'))

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)


class MyUserManager(BaseUserManager):
    """ A customer Manager to deal with emails as unique identifier """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(gettext_lazy('staff status'), default=False,
                                   help_text=gettext_lazy('Designates whether the user can log in this site'))
    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True,
        help_text=gettext_lazy('Designates whether this user should be treated as active')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class SkillCategoryModel(models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.categoryName}"


class SkillListModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_skill_list')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategoryModel, on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return f"skill --> {self.title}"


class EducationModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_education')
    level_of_education = models.CharField(max_length=200)
    starting_year = models.DateField(default='2000-01-01')
    passing_year = models.DateField(default='2000-01-01', blank=True, null=True)
    active = models.BooleanField(default=False)
    major_subjects = models.CharField(max_length=255)
    minor_subjects = models.CharField(max_length=255, blank=True, null=True)
    CGPA = models.CharField(max_length=5, blank=True, null=True)
    institution = models.CharField(max_length=200)

    def __str__(self):
        return self.level_of_education


class Extra_curricular_Activities_Model(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_extra_curricular')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.topic


class Co_curricular_Activities_Model(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_co_curricular')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.topic


class AchievementModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_achievements')
    topic = models.CharField(max_length=254)
    perform_time = models.DateField(default='2000-01-01')


class ExperiencesModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_experiences')
    position = models.CharField(max_length=100)
    starting_year = models.DateField(default='2000-01-01')
    leaving_year = models.DateField(default='2000-01-01', blank=True, null=True)
    location = models.CharField(max_length=200)
    Company = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.user}'s experiences on {self.Company} as a/an {self.position}"


class ReferencesModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='user_references')
    name_of_reference = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    contact = models.CharField(validators=[phone_regex], max_length=14)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s reference name is {self.name_of_reference}"


class Profile_main(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_main_profile')
    career_objective = models.TextField(default="Opportunities don't happen, You create them. ")
    fullName = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=14)
    ID_card = models.ImageField(upload_to='id_card/')
    profile_picture = models.ImageField(upload_to='user_profile_picture/')
    Date_of_Birth = models.DateField(default='2000-01-01')
    gender = models.CharField(choices=gender, max_length=10)
    house_no = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.PositiveIntegerField(default=1200)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')
    created_date = models.DateField(auto_now_add=True)

