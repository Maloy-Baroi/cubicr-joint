from django.contrib import admin
from App_auth.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Profile_main)
admin.site.register(ReferencesModel)
admin.site.register(ExperiencesModel)
admin.site.register(Co_curricular_Activities_Model)
admin.site.register(Extra_curricular_Activities_Model)
admin.site.register(EducationModel)
admin.site.register(SkillCategoryModel)
admin.site.register(SkillListModel)

