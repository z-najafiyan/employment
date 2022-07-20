from django.core.validators import RegexValidator
from django.db import models

from common.models import (User, Province, Category, Skill)
from constant.views import (MARITAL_STATUS, GENDER, MONTH, GRADE, MASTERY_LEVEL, LANGUAGE_NAME, TYPE_COOPERATION,
                                DEGREE_OF_EDUCATIONS, LEVEL, SALARY, JOB_BENEFITS)


# Create your models here.


class Education(models.Model):
    field_of_study = models.CharField(max_length=500, )
    name_university = models.CharField(max_length=500)
    grade = models.CharField(max_length=100, choices=GRADE)
    start_years = models.CharField(max_length=4)
    end_years = models.CharField(max_length=4)
    is_student = models.BooleanField()
    description = models.CharField(max_length=2000)

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class Language(models.Model):
    name = models.CharField(choices=LANGUAGE_NAME, max_length=20)
    mastery_level = models.CharField(choices=MASTERY_LEVEL, max_length=20)

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class WorkExperience(models.Model):
    job_title = models.CharField(max_length=500, )
    company_name = models.CharField(max_length=1000)
    start_month = models.CharField(max_length=2, choices=MONTH)
    start_years = models.CharField(max_length=4, validators=[RegexValidator(r"[1][3-4][0-9][0-9]")])
    end_month = models.CharField(max_length=2, choices=MONTH, null=True, blank=True, )
    end_years = models.CharField(max_length=4, null=True, blank=True,
                                 validators=[RegexValidator(r"[1][3-4][0-9][0-9]")])
    is_employed = models.BooleanField()
    description = models.CharField(max_length=2000)

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class PersonalInfo(models.Model):
    # province = models.ForeignKey(Province, null=True, blank=True, related_name="personal_infos",
    #                              related_query_name="personal_info", on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(max_length=20000, null=True, )
    years_birth = models.CharField(max_length=4, )
    gender = models.CharField(choices=GENDER, max_length=500, null=True, blank=True)
    marital_status = models.CharField(choices=MARITAL_STATUS, max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class JobBenefits(models.Model):
    name = models.CharField(choices=JOB_BENEFITS, max_length=2000, unique=True)

    def __str__(self):
        return f"id{self.id}__name:{self.name}"

    class Meta:
        ordering = ["-id"]


class JobPreference(models.Model):
    province = models.ForeignKey(Province, null=True, blank=True, related_name="job_preferences",
                                 related_query_name="job_preference", on_delete=models.CASCADE)
    type_cooperation = models.CharField(choices=TYPE_COOPERATION, max_length=500, null=True, blank=True)
    mastery_level = models.CharField(choices=LEVEL, max_length=500, null=True, blank=True)
    minimum_salary = models.CharField(max_length=500, choices=SALARY, null=True, blank=True)
    degree_of_educations = models.CharField(choices=DEGREE_OF_EDUCATIONS, max_length=500, null=True, blank=True)
    job_benefits = models.ManyToManyField(JobBenefits)

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class Resume(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="resumes", related_query_name="resume",
                                 on_delete=models.CASCADE, null=True, blank=True
                                 )
    file = models.FileField(upload_to='', blank=True, null=True)
    education = models.ManyToManyField(Education, related_name="resumes", related_query_name="resume", )
    personal_info = models.ForeignKey(PersonalInfo, related_name="resumes", related_query_name="resume",
                                      on_delete=models.CASCADE, null=True, blank=True)
    skill = models.ManyToManyField(Skill, related_name="resumes", related_query_name="resume")
    job_preferences = models.ForeignKey(JobPreference, related_name="resumes", related_query_name="resume",
                                        on_delete=models.CASCADE, null=True, blank=True)
    work_experience = models.ManyToManyField(WorkExperience, related_name="resumes", related_query_name="resume", )
    about_me = models.TextField(max_length=20000, null=True, blank=True)

    language=models.ManyToManyField(Language,related_name="resumes", related_query_name="resume",)

    def __str__(self):
        return f"id:{self.id}"

    class Meta:
        ordering = ["-id"]


class Candidate(models.Model):
    user = models.ForeignKey(User, related_name="candidates", related_query_name="candidate", on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, related_name="candidates", related_query_name="candidate",
                               on_delete=models.CASCADE)
    mobile = models.CharField(max_length=11, null=True, blank=True)


    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]


class MarkedAnnouncement(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="marked_announcements",
                                  related_query_name="marked_announcement",
                                  on_delete=models.CASCADE)

    announcement = models.ManyToManyField("employer.Announcement")

    def __str__(self):
        return f"id{self.id}"

    class Meta:
        ordering = ["-id"]
