from rest_framework import serializers

from candidate.models import Candidate, Resume, Education, PersonalInfo, WorkExperience, JobPreference, JobBenefits
from common.models import User, Category, Skill
from employer.models import Company, Announcement, StatusLog, Applicant, Employer
from other_files.response_serialzer import CityResponseSerializer, ProvinceResponseSerializer, \
    ActivityResponseSerializer, UserResponseSerializer, CategoryResponseSerializer


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
    number_employees = serializers.SerializerMethodField()
    logo = serializers.CharField(source="link", default=None)

    class Meta:
        model = Company
        fields = "__all__"

    def get_number_employees(self, obj):
        if obj.number_employees:
            return {"en_name": obj.number_employees,
                    "fa_name": obj.get_number_employees_display()}
        return None


class EmployerAnnouncementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        exclude = ["creator_user", "company", "applicant"]


class EmployerAnnouncementListSerializer(serializers.ModelSerializer):
    number_not_checked = serializers.SerializerMethodField()
    number_awaiting_status = serializers.SerializerMethodField()
    number_confirmation = serializers.SerializerMethodField()
    number_hired = serializers.SerializerMethodField()
    number_rejected = serializers.SerializerMethodField()
    province = ProvinceResponseSerializer()
    category = CategoryResponseSerializer()

    class Meta:
        model = Announcement
        fields = ["id","title", "category", "number_not_checked", "number_awaiting_status",
                  "number_confirmation", "number_hired", "number_rejected", "province"
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
    creation_date = serializers.IntegerField(source="creation_date_ts", default=None)
    province=ProvinceResponseSerializer()
    class Meta:
        model = Announcement
        fields = ["id", "title", "creation_date", "province"]


class EmployerUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "id"]


class EmployerPersonalInfoGetSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="link", default=None)

    class Meta:
        model = PersonalInfo
        fields = ["image", "id"]


class EmployerResumeGetSerializer(serializers.ModelSerializer):
    personal_info = EmployerPersonalInfoGetSerializer()

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
    created_date_time = serializers.IntegerField(source="created_date_time_ts", default=None)
    applicant_status = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = ["applicant_status", "candidate", "created_date_time", "id"]

    def get_applicant_status(self, obj):
        if obj.applicant_status:
            return {'fa_name': obj.get_applicant_status_display(),
                    "en_name": obj.applicant_status}
        return None


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
    # province = ProvinceResponseSerializer()

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

    # job_benefits = EmployerJobBenefitsDetailSerializer(many=True)

    class Meta:
        model = JobPreference
        fields = "__all__"


class EmployerWorkExperienceDetailSerializer(serializers.ModelSerializer):
    start_date = serializers.IntegerField(source="start_date_ts", default=None)
    end_date = serializers.IntegerField(source="end_date_ts", default=None)

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
    file = serializers.CharField(source="link", allow_null=True)

    class Meta:
        model = Resume
        fields = "__all__"


class EmployerCandidateDeleteSerializer(serializers.ModelSerializer):
    user = EmployerUserDetailSerializer()
    resume = EmployerResumeDetailSerializer()

    class Meta:
        model = Candidate
        fields = "__all__"
