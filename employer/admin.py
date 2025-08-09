from django.contrib import admin

from employer.models import (Activity,
                             Company,
                             Employer, Applicant, Announcement, StatusLog, Score,
                             )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "persian_name", "province"]
    list_display_links = ["id", "persian_name", "province"]
    search_fields = ["id", "persian_name", "province"]
    filter_fields = ["id", "persian_name", "province"]

    def province(self, obj: Company):
        try:
            return obj.province.id
        except AttributeError:
            return None


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ["id", "company", "user"]
    list_display_links = ["id", "company", "user"]
    search_fields = ["id", "company", "user"]

    def company(self, obj: Employer):
        try:
            return obj.company.id
        except AttributeError:
            return None

    def user(self, obj: Employer):
        try:
            return obj.user.id
        except AttributeError:
            return None


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = ["id", "applicant_status", "candidate"]
    list_display_links = ["id", "applicant_status", "candidate"]
    search_fields = ["id", "applicant_status", "candidate"]

    def candidate(self, obj: Applicant):
        try:
            return obj.candidate.id
        except AttributeError:
            return None


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "category", "status_name"]
    list_display_links = ["id", "title", "category", "status_name"]
    search_fields = ["id", "title", "category", "status_name"]

    def company(self, obj: Announcement):
        try:
            return obj.category.name
        except AttributeError:
            return None


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "announcement", "applicant_status"]
    list_display_links = ["id", "candidate", "announcement", "applicant_status"]
    search_fields = ["id", "candidate", "announcement", "applicant_status"]

    def candidate(self, obj: StatusLog):
        try:
            return obj.candidate.id
        except AttributeError:
            return None

    def announcement(self, obj: StatusLog):
        try:
            return obj.announcement.id
        except AttributeError:
            return None


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ["id", "candidate", "announcement", "score"]
    list_display_links = ["id", "candidate", "announcement", "score"]
    search_fields = ["id", "candidate", "announcement", "score"]
