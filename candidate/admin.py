from django.contrib import admin

from candidate.models import (Education,
                              Language,
                              WorkExperience,
                              PersonalInfo,
                              JobBenefits,
                              JobPreference,
                              Resume,
                              Candidate,
                              MarkedAnnouncement, ProfessionalSkill, )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["id", "field_of_study", "name_university", "grade"]
    list_display_links = ["id", "field_of_study", "name_university", "grade"]
    search_fields = ["id", "field_of_study", "name_university", "grade"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "mastery_level"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name", "mastery_level"]


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ["id", "job_title", "company_name", "start_date", "end_date"]
    list_display_links = ["id", "job_title", "company_name", "start_date", "end_date"]
    search_fields = ["id", "job_title", "company_name"]


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ["id", "years_birth", "gender"]
    list_display_links = ["id", "years_birth", "gender"]
    search_fields = ["id", "years_birth", "gender"]


@admin.register(JobBenefits)
class JobBenefitsAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(JobPreference)
class JobPreferenceAdmin(admin.ModelAdmin):
    list_display = ["id"]
    list_display_links = ["id"]
    search_fields = ["id"]


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ["id", "personal_info", "skill"]
    list_display_links = ["id"]
    search_fields = ["id", "education", "personal_info", "skill", "job_preferences", "work_experience"]

    def skill(self, obj):
        return [p.id for p in obj.professional_skill.all()]


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "resume"]
    list_display_links = ["id", "user", "resume"]
    search_fields = ["id", "user", "resume"]


@admin.register(MarkedAnnouncement)
class MarkedAnnouncementAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "announcement"]
    list_display_links = ["id", "candidate"]
    search_fields = ["id", "candidate", "announcement"]

    def announcement(self, obj):
        return [p.id for p in obj.announcement.all()]
@admin.register(ProfessionalSkill)
class ProfessionalSkillAdmin(admin.ModelAdmin):
    list_display = ["id", "skill", ]
    list_display_links = ["id", ]
    search_fields = ["id", "skill"]