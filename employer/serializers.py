from rest_framework import serializers

from candidate.models import Candidate, Resume, Education, PersonalInfo, WorkExperience, JobPreference, JobBenefits
from common.models import User, Category, Skill
from employer.models import Company, Announcement, StatusLog, Applicant, Employer
from other_files.response_serialzer import CityResponseSerializer, ProvinceResponseSerializer, \
    ActivityResponseSerializer, UserResponseSerializer


class EmployerUserPostSerializer(serializers.ModelSerializer):
    # sing_up
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        obj = User.objects.create_user(**validated_data)
        return obj

    def validate_email(self, value):
        """
        Check that the email filed is unique
        """
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError("This field must be unique")
        return value


class EmployerUserPostV2Serializer(serializers.ModelSerializer):
    # sing_in
    class Meta:
        model = User
        fields = ["email", "password"]


class EmployerSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer()

    class Meta:
        model = Employer
        fields = "__all__"


class EmployerCompanyPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class EmployerCompanyGetSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()
    city = CityResponseSerializer()
    activity = ActivityResponseSerializer()

    class Meta:
        model = Company
        fields = "__all__"


class EmployerAnnouncementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        exclude = ["creator_user", "company"]


class EmployerAnnouncementListSerializer(serializers.ModelSerializer):
    number_not_checked = serializers.SerializerMethodField()
    number_awaiting_status = serializers.SerializerMethodField()
    number_confirmation = serializers.SerializerMethodField()
    number_hired = serializers.SerializerMethodField()
    number_rejected = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ["title", "category", "status_name", "number_not_checked", "number_awaiting_status",
                  "number_confirmation", "number_hired",
                  ]

    def get_number_not_checked(self, obj):
        number = StatusLog.objects.filter(announcement=obj, applicant_status="not_checked").count()
        return number

    def get_number_awaiting_status(self, obj):
        number = StatusLog.objects.filter(announcement=obj, applicant_status="awaiting_status").count()
        return number

    def get_number_confirmation(self, obj):
        number = StatusLog.objects.filter(announcement=obj, applicant_status="confirmation_for_interview").count()
        return number

    def get_number_hired(self, obj):
        number = StatusLog.objects.filter(announcement=obj, applicant_status="hired").count()
        return number

    def get_number_rejected(self, obj):
        number = StatusLog.objects.filter(announcement=obj, applicant_status="rejected").count()
        return number


class EmployerAnnouncementGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        exclude = ["creator_user", "company"]


class EmployerUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "id"]


class EmployerResumeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["title", "id"]


class EmployerCandidateGetSerializer(serializers.ModelSerializer):
    user = EmployerUserGetSerializer()
    resume = EmployerResumeGetSerializer()

    class Meta:
        model = Candidate
        fields = ["user", "resume", "id"]


class EmployerApplicantGetSerializer(serializers.ModelSerializer):
    candidate = EmployerCandidateGetSerializer()

    class Meta:
        model = Applicant
        fields = ["applicant_status", "candidate", "created_date_time"]


class EmployerApplicantPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["applicant_status", "id"]


class EmployerUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class EmployerCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class EmployerEducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class EmployerPersonalInfoDetailSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()

    class Meta:
        model = PersonalInfo
        fields = "__all__"


class EmployerSkillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class EmployerJobBenefitsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobBenefits
        fields = "__all__"


class EmployerJobPreferencesDetailSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()
    job_benefits = EmployerJobBenefitsDetailSerializer(many=True)

    class Meta:
        model = JobPreference
        fields = "__all__"


class EmployerWorkExperienceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"


class EmployerResumeDetailSerializer(serializers.ModelSerializer):
    category = EmployerCategoryDetailSerializer()
    education = EmployerEducationDetailSerializer(many=True)
    personal_info = EmployerPersonalInfoDetailSerializer()
    skill = EmployerSkillDetailSerializer(many=True)
    job_preferences = EmployerJobPreferencesDetailSerializer()
    work_experience = EmployerWorkExperienceDetailSerializer(many=True)

    class Meta:
        model = Resume
        fields = "__all__"


class EmployerCandidateDeleteSerializer(serializers.ModelSerializer):
    user = EmployerUserDetailSerializer()
    resume = EmployerResumeDetailSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"
