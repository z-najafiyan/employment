from rest_framework import serializers

from candidate.models import JobBenefits
from common.models import Province, City, User, Category
from employer.models import Activity


class ProvinceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class CityResponseSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()

    class Meta:
        model = City
        fields = "__all__"


class JobBenefitsResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = JobBenefits
        fields = "__all__"

    def get_name(self, obj):
        if obj.name:
            return {"en_name": obj.name,
                    "fa_name": obj.get_name_display()}
        return None


class ActivityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class UserResponseSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "role"]

    def get_role(self, obj):
        role = obj.groups.all()[0].name
        return role


# class EducationResponseSerializer(serializers.ModelSerializer):
#     grade = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Education
#         fields = ["id", "field_of_study", "name_university", "grade", "start_years", "end_years", "is_student",
#                   "description"]
#
#     def get_grade(self, obj):
#         return {"en_name": obj.grade,
#                 "fa_name": obj.get_grade_display()}

class CategoryResponseSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "__all__"

    def get_name(self, obj):
        if obj.name:
            return {"en_name": obj.name,
                    "fa_name": obj.get_name_display()}
        return None


class UserTokenSwaggerSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=3000)
    access = serializers.CharField(max_length=3000)
