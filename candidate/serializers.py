from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from candidate.models import (MarkedAnnouncement, Education, JobPreference, Resume, WorkExperience, PersonalInfo,
                              Candidate)
from common.models import (User, Skill)
from employer.models import (Announcement, Company, Applicant)
from other_files.response_serialzer import (ProvinceResponseSerializer, JobBenefitsResponseSerializer,
                                            UserResponseSerializer, CategoryResponseSerializer, )


class CandidateUserPostSerializer(serializers.ModelSerializer):
    # sing_up
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]

    def validate_email(self, value):
        """
        Check that the email filed is unique
        """
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError("This field must be unique")
        return value

    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        return obj


class CandidateUserSingInSerializer(serializers.ModelSerializer):
    # sing_in
    class Meta:
        model = User
        fields = ["email", "password"]


class CandidateSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer()

    class Meta:
        model = Candidate
        fields = ["user", "resume"]


class CandidateEducationPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "field_of_study", "name_university", "grade", "start_years", "end_years", "is_student",
                  "description", "resumes"]


class CandidateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name", "resumes"]


class CandidateJobPreferencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPreference
        fields = ["resumes", "province", "type_cooperation", "mastery_level", "minimum_salary", "degree_of_educations",
                  "job_benefits", "id"]


class CandidateJobPreferenceGetSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()
    job_benefits = JobBenefitsResponseSerializer(many=True)
    type_cooperation = serializers.SerializerMethodField()
    mastery_level = serializers.SerializerMethodField()
    minimum_salary = serializers.SerializerMethodField()
    degree_of_educations = serializers.SerializerMethodField()

    class Meta:
        model = JobPreference
        fields = "__all__"

    def get_type_cooperation(self, obj):
        if obj.type_cooperation:
            return {"en_name": obj.type_cooperation,
                    "fa_name": obj.get_type_cooperation_display()}
        return None

    def get_mastery_level(self, obj):
        if obj.mastery_level:
            return {"en_name": obj.mastery_level,
                    "fa_name": obj.get_mastery_level_display()}
        return None

    def get_minimum_salary(self, obj):
        if obj.minimum_salary:
            return {"en_name": obj.minimum_salary,
                    "fa_name": obj.get_minimum_salary_display()}
        return None

    def get_degree_of_educations(self, obj):
        if obj.degree_of_educations:
            return {"en_name": obj.degree_of_educations,
                    "fa_name": obj.get_degree_of_educations_display()}
        return None


class CandidateEducationGETSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = ["id", "field_of_study", "name_university", "grade", "start_years", "end_years", "is_student",
                  "description", ]

    def get_grade(self, obj):
        return {"en_name": obj.grade,
                "fa_name": obj.get_grade_display()}


class CandidatePersonalInfoGETSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()
    gender = serializers.SerializerMethodField()
    marital_status = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInfo
        fields = "__all__"

    def get_gender(self, obj):
        if obj.gender:
            return {"en_name": obj.gender,
                    "fa_name": obj.get_gender_display()}
        return None

    def get_marital_status(self, obj):
        if obj.marital_status:
            return {"en_name": obj.marital_status,
                    "fa_name": obj.get_marital_status_display()}
        return None


class CandidateWorkExperienceGetSerializer(serializers.ModelSerializer):
    start_month = serializers.SerializerMethodField()
    end_month = serializers.SerializerMethodField()

    class Meta:
        model = WorkExperience
        fields = "__all__"

    def get_start_month(self, obj):
        if obj.start_month:
            return {"en_name": obj.start_month,
                    "fa_name": obj.get_start_month_display()}
        return None

    def get_end_month(self, obj):
        if obj.end_month:
            return {"en_name": obj.end_month,
                    "fa_name": obj.get_end_month_display()}
        return None


class CandidateWorkExperiencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ["id", "resumes", "job_title", "company_name", "start_month", "start_years", "end_month", "end_years",
                  "is_employed", "description"]

    def validate_end_month(self, value):
        if not self.initial_data["is_employed"]:
            if not value:
                raise serializers.ValidationError("This field may not be null")
        return value

    def validate_end_years(self, value):
        if not self.initial_data["is_employed"]:
            if not value:
                raise serializers.ValidationError("This field may not be null")
        return value


class CandidateResumeGETSerializer(serializers.ModelSerializer):
    category = CategoryResponseSerializer()
    file = serializers.SerializerMethodField()
    education = CandidateEducationGETSerializer(many=True)
    personal_info = CandidatePersonalInfoGETSerializer()
    skill = CandidateSkillSerializer(many=True)
    job_preferences = CandidateJobPreferenceGetSerializer()
    work_experience = CandidateWorkExperienceGetSerializer(many=True)

    class Meta:
        model = Resume
        fields = "__all__"

    def get_category(self, obj):
        if obj.category:
            res = {"en_name": obj.category,
                   "fa_name": obj.get_category_display()}

        return None

    def get_file(self, obj):
        return None


class CandidateResumePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["title", "category", "file"]


class CandidatePersonalInfoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["province", "address", "years_birth", "gender", "about_me", "marital_status", "resumes"]


class CandidateCompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['persian_name', "english_name", "logo", "activity"]


class CandidateAnnouncementListSerializer(serializers.ModelSerializer):
    company = CandidateCompanyListSerializer()

    class Meta:
        model = Announcement
        fields = ["title", "province", "city", "type_cooperation", "minimum_salary", "company"]


class CandidateCompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CandidateAnnouncementDetailSerializer(serializers.ModelSerializer):
    company = CandidateCompanyListSerializer()

    class Meta:
        model = Announcement
        fields = ["title", "province", "city", "type_cooperation", "minimum_salary", "company"]


class CandidateMarkedAnnouncementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkedAnnouncement
        fields = ["announcement"]


class CandidateApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        models = Applicant
        fields = ['candidate']


class CandidateAnnouncementPatchSerializer(WritableNestedModelSerializer):
    applicant = CandidateApplicantCreateSerializer()

    class Meta:
        models = Announcement
        fields = ["applicant"]
