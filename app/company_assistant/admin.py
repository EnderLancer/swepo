from django.contrib import admin

from django.contrib import admin

from .models import (
    Employer,
    Company,
    ProcessCategory,
    SwdProcess,
    SpecificPracticeWeightRelation,
    CompanySpecific,
    ProcessPractice
)

admin.site.register(Employer)
admin.site.register(Company)
admin.site.register(ProcessCategory)
admin.site.register(SwdProcess)
admin.site.register(SpecificPracticeWeightRelation)
admin.site.register(CompanySpecific)
admin.site.register(ProcessPractice)