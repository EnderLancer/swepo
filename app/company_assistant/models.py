import logging

from django.db import models
from django.contrib.auth import get_user_model


LOGGER = logging.getLogger(__name__)


User = get_user_model()

class Employer(models.Model):
    """
    Represents a company's employer which has access to process assessments
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employer")


class ProcessCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(max_length=500, default="", blank=True)


class SwdProcess(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(ProcessCategory, related_name="processes", on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=500, default="", blank=True)


class ProcessPractice(models.Model):
    name = models.CharField(max_length=50, unique=True)
    process = models.ForeignKey(SwdProcess, related_name="practices", on_delete=models.CASCADE)
    description = models.TextField(max_length=500, default="", blank=True)


class Specific(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500, default="", blank=True)


class Company(models.Model):
    """
    An object which used to evaluate processes capability of working company 
    """
    name = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=500, default="")
    created_by = models.ForeignKey(Employer, related_name="creted_companies", on_delete=models.DO_NOTHING)
    followers = models.ManyToManyField(Employer, related_name="followed_companies", blank=True)
    specifics = models.ManyToManyField(Specific, through="CompanySpecific", blank=True)


class CompanySpecific(models.Model):
    company = models.ForeignKey(Company, models.CASCADE)
    specific = models.ForeignKey(Specific, models.CASCADE)
    score = models.SmallIntegerField(null=False)


class SpecificPracticeWeightRelation(models.Model):
    specific = models.ForeignKey(Specific, models.DO_NOTHING)
    practice = models.ForeignKey(ProcessPractice, models.DO_NOTHING)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    reason = models.TextField(max_length=500, blank=True, null=True)
