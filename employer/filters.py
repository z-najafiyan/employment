from django.db.models import Q
from django_filters import rest_framework

from employer.models import Announcement, Applicant


class AnnouncementFilter(rest_framework.FilterSet):
    title = rest_framework.CharFilter(lookup_expr="icontains")
    category = rest_framework.CharFilter(method="category_filter")
    province = rest_framework.CharFilter(method="province_filter")
    city = rest_framework.CharFilter(method="city_filter")
    type_cooperation = rest_framework.CharFilter(lookup_expr="icontains")
    minimum_SALARY = rest_framework.CharFilter(lookup_expr="icontains")
    degree_of_educations = rest_framework.CharFilter(lookup_expr="icontains")
    gender = rest_framework.CharFilter(lookup_expr="icontains")
    military_service = rest_framework.CharFilter(lookup_expr="icontains")
    applicant = rest_framework.CharFilter(method="applicant_filter")
    status_name = rest_framework.CharFilter(lookup_expr="icontains")
    active_time = rest_framework.CharFilter(lookup_expr="icontains")
    several_variable = rest_framework.CharFilter(method="several_variable_filter")

    def category_filter(self, queryset, value, name):
        return queryset.filter(category_id=value)

    def province_filter(self, queryset, value, name):
        return queryset.filter(province_id=value)

    def city_filter(self, queryset, value, name):
        return queryset.filter(city_id=value)

    def applicant_filter(self, queryset, value, name):
        return queryset.filter(applicant_id=value)

    def several_variable_filter(self, queryset, value, name):
        queryset = queryset.filter(Q(category__name__icontains=value) |
                                   Q(category__fa_name__icontains=value) |
                                   Q(title__icontains=value) |
                                   Q(skill__name__icontains=value)).distinct()
        return queryset

    class Meta:
        model = Announcement
        fields = ["title", "category", "province", "city", "type_cooperation", "minimum_salary", "degree_of_educations",
                  "gender", "military_service", "applicant", "status_name", "active_time","several_variable"]


class ApplicantFilter(rest_framework.FilterSet):
    applicant_status = rest_framework.CharFilter(lookup_expr="icontains")
    gender = rest_framework.CharFilter(method="gender_filter")
    province = rest_framework.CharFilter(method="province_filter")

    def gender_filter(self, queryset, value, name):
        return queryset.filter(candidate__resume__personal_info__gender=value)

    def province_filter(self, queryset, value, name):
        return queryset.filter(candidate__resume__personal_info__province_id=value)

    class Meta:
        model = Applicant
        fields = ["applicant_status", "gender", "province"]
