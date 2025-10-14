from django.contrib import admin
from .models import Organization, EducationInstitution, SupportMeasure, Specialty, Roadmap, UserPath

admin.site.register(Organization)
admin.site.register(EducationInstitution)
admin.site.register(SupportMeasure)
admin.site.register(Specialty)
admin.site.register(Roadmap)
admin.site.register(UserPath)
#пусть будет