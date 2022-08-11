import datetime
import time

from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
from candidate.models import Candidate, Skill
from common.models import (User, City, Province, Category)
from constant.views import (ANNOUNCEMENT_STATUS,
                            DEGREE_OF_EDUCATIONS,
                            TYPE_COOPERATION,
                            MILITARY_SERVICE,
                            APPLICANT_STATUS,
                            GENDER, NUMBER_EMPLOYEES, YEARS_WORK_EXPERIENCE,
                            )
from employment import settings


def timestamp(date):
    return time.mktime(date.timetuple())


class Activity(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return f"id:{self.id}--name:{self.name}"

    class Meta:
        ordering = ["-id"]


class Company(models.Model):
    persian_name = models.CharField(max_length=1000, null=True, blank=True)
    english_name = models.CharField(max_length=1000, null=True, blank=True)
    logo = models.ImageField(upload_to="", null=True)
    province = models.ForeignKey(Province, related_name="companies", related_query_name="company",
                                 on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, related_name="companies", related_query_name="company", on_delete=models.CASCADE,
                             null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    activity = models.ForeignKey(Activity, related_name="companies", related_query_name="company",
                                 on_delete=models.CASCADE, null=True, blank=True)

    address = models.TextField(max_length=4000, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=20000, null=True, blank=True)
    number_employees = models.CharField(choices=NUMBER_EMPLOYEES, max_length=500, blank=True, null=True)

    def __str__(self):
        return f"id:{self.id}--name:{self.persian_name}"

    class Meta:
        ordering = ["-id"]

    @property
    def link(self, ):
        if self.logo:
            return f"{settings.IMAGE_URL_SERVE}{settings.MEDIA_URL}{self.logo}"
        return None


class Employer(models.Model):
    company = models.ForeignKey(Company, null=True, blank=True, related_name="employers", related_query_name="employer",
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="employers", related_query_name="employer", on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.id}"

    class Meta:
        ordering = ["-id"]


class Applicant(models.Model):
    applicant_status = models.CharField(choices=APPLICANT_STATUS, max_length=500, default="not_checked")
    candidate = models.ForeignKey(Candidate, related_name="applicants", related_query_name="applicant",
                                  on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id:{self.id}"

    @property
    def created_date_time_ts(self):
        if self.created_date_time:
            return timestamp(self.created_date_time) * 1000
        return None

    class Meta:
        ordering = ["-id"]


class Announcement(models.Model):
    title = models.CharField(max_length=500, )
    category = models.ForeignKey(Category, related_name="announcements", related_query_name="announcement",
                                 on_delete=models.CASCADE, )
    province = models.ForeignKey(Province, related_name="announcements", related_query_name="announcement",
                                 on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name="announcements", related_query_name="announcement",
                             on_delete=models.CASCADE)
    type_cooperation = models.CharField(choices=TYPE_COOPERATION, max_length=500)
    minimum_salary = models.CharField(max_length=500, null=True, blank=True)
    degree_of_educations = models.CharField(choices=DEGREE_OF_EDUCATIONS, max_length=500, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=500, null=True, blank=True)
    military_service = models.CharField(choices=MILITARY_SERVICE, max_length=500, null=True, blank=True)
    applicant = models.ManyToManyField("Applicant",blank=True)
    status_name = models.CharField(choices=ANNOUNCEMENT_STATUS, max_length=500, default="active")
    active_time = models.IntegerField(MaxValueValidator(100), default=100)
    creation_date = models.DateTimeField(auto_now=True)
    creator_user = models.ForeignKey(User, related_name="announcements", related_query_name="announcement",
                                     on_delete=models.CASCADE)
    # skill = models.ManyToManyField(Skill, )
    description = models.TextField(max_length=10000, null=True, blank=True)
    company = models.ForeignKey(Company, related_name="announcements", related_query_name="announcement",
                                on_delete=models.CASCADE)
    years_work_experience = models.CharField(choices=YEARS_WORK_EXPERIENCE, max_length=500, default="unlimited")

    def __str__(self):
        return f"id:{self.id}--name:{self.title}"

    @property
    def creation_days(self):
        date_now = datetime.datetime.now()
        diff = date_now - self.creation_date
        # diff_in_day = diff / 3600 * 24
        # return diff_in_day
        return diff.days

    class Meta:
        ordering = ["-id"]

    @property
    def creation_date_ts(self):
        if self.creation_date:
            return timestamp(self.creation_date) * 1000
        return None


class StatusLog(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="status_log", related_query_name="status_logs",
                                  on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, related_name="status_log", related_query_name="status_logs",
                                     on_delete=models.CASCADE)
    applicant_status = models.CharField(choices=APPLICANT_STATUS, max_length=500, default="not_checked")
    user = models.ForeignKey(User, related_name="status_log", related_query_name="status_logs",
                             on_delete=models.CASCADE)
    created_date_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id:{self.id}--name:{self.applicant_status}"

    class Meta:
        ordering = ["-id"]

    @property
    def created_date_time_ts(self):
        if self.created_date_time:
            return timestamp(self.created_date_time) * 1000
        return None
