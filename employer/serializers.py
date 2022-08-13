from rest_framework import serializers

from candidate.models import Candidate, Resume, Education, PersonalInfo, WorkExperience, JobPreference, JobBenefits, \
    ProfessionalSkill, Language
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
        fields = ["id", "title", "category", "number_not_checked", "number_awaiting_status",
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
    province = ProvinceResponseSerializer()
    status_name = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ["id", "title", "creation_date", "province", "status_name"]

    def get_status_name(self, obj):
        if obj.status_name:
            return {'fa_name': obj.get_status_name_display(),
                    "en_name": obj.status_name}
        return None


class EmployerUserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "id"]


class EmployerPersonalInfoGetSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source="link", default=None)
    category = CategoryResponseSerializer()

    class Meta:
        model = PersonalInfo
        fields = ["image", "category", "id"]


class EmployerResumeGetSerializer(serializers.ModelSerializer):
    personal_info = EmployerPersonalInfoGetSerializer()

    class Meta:
        model = Resume
        fields = ["personal_info", "id"]


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
    grade = serializers.SerializerMethodField()
    start_date = serializers.IntegerField(source="start_date_ts", default=None)
    end_date = serializers.IntegerField(source="end_date_ts", default=None)

    class Meta:
        model = Education
        fields = "__all__"

    def get_grade(self, obj):
        if obj.grade:
            return {"en_name": obj.grade,
                    "fa_name": obj.get_grade_display()}


class EmployerPersonalInfoDetailSerializer(serializers.ModelSerializer):
    # province = ProvinceResponseSerializer()
    category = CategoryResponseSerializer()
    gender = serializers.SerializerMethodField()
    marital_status = serializers.SerializerMethodField()
    military_status = serializers.SerializerMethodField()
    image = serializers.CharField(source="link", default=None)

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

    def get_military_status(self, obj):
        if obj.military_status:
            return {"en_name": obj.military_status,
                    "fa_name": obj.get_military_status_display()}
        return None

    def get_minimum_salary(self, obj):
        if obj.minimum_salary:
            return {"en_name": obj.minimum_salary,
                    "fa_name": obj.get_minimum_salary_display()}
        return None


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
    type_cooperation = serializers.SerializerMethodField()
    mastery_level = serializers.SerializerMethodField()
    minimum_salary = serializers.SerializerMethodField()
    degree_of_educations = serializers.SerializerMethodField()

    # job_benefits = EmployerJobBenefitsDetailSerializer(many=True)

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


class EmployerWorkExperienceDetailSerializer(serializers.ModelSerializer):
    start_date = serializers.IntegerField(source="start_date_ts", default=None)
    end_date = serializers.IntegerField(source="end_date_ts", default=None)

    class Meta:
        model = WorkExperience
        fields = "__all__"


class EmployerProfessionalSkillDetailSerializer(serializers.ModelSerializer):
    # skill = EmployerSkillDetailSerializer()
    mastery_level = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalSkill
        fields = "__all__"

    def get_mastery_level(self, obj):
        if obj.mastery_level:
            return {"en_name": obj.mastery_level,
                    "fa_name": obj.get_mastery_level_display()}
        return None

class EmployerLanguageGetSerializer(serializers.ModelSerializer):
    mastery_level=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    class Meta:
        model = Language
        fields = ["id", "name", "mastery_level",]
    def get_mastery_level(self, obj):
        if obj.mastery_level:
            return {"en_name": obj.mastery_level,
                    "fa_name": obj.get_mastery_level_display()}
        return None
    def get_name(self, obj):
        if obj.name:
            return {"en_name": obj.name,
                    "fa_name": obj.get_name_display()}
        return None

class EmployerResumeDetailSerializer(serializers.ModelSerializer):
    education = EmployerEducationDetailSerializer(many=True)
    personal_info = EmployerPersonalInfoDetailSerializer()
    professional_skill = EmployerProfessionalSkillDetailSerializer(many=True)
    job_preferences = EmployerJobPreferencesDetailSerializer()
    work_experience = EmployerWorkExperienceDetailSerializer(many=True)
    file = serializers.CharField(source="link", allow_null=True)
    employment_status=serializers.SerializerMethodField()
    language=EmployerLanguageGetSerializer(many=True)
    class Meta:
        model = Resume
        fields = ["id","file","education","personal_info","professional_skill","job_preferences","work_experience",
                  "about_me","language","employment_status"]
    def get_employment_status(self,obj):
        is_employed = obj.work_experience.all()[0].is_employed
        if is_employed:
            return "به دنبال شغلی بهتر"
        return "جویای کار"


class EmployerCandidateDeleteSerializer(serializers.ModelSerializer):
    user = EmployerUserDetailSerializer()
    resume = EmployerResumeDetailSerializer()
    applicant_status=serializers.SerializerMethodField()
    created_date_time=serializers.SerializerMethodField()
    class Meta:
        model = Candidate
        fields = ["user","resume","mobile","email","applicant_status","id","created_date_time"]
    def get_applicant_status(self,obj):
        applicant=self.context["applicant"]
        if applicant.applicant_status:
            return {"en_name": applicant.applicant_status,
                    "fa_name": applicant.get_applicant_status_display()}
        return None
    def get_created_date_time(self,obj):
        applicant = self.context["applicant"]
        if applicant.created_date_time:
            return applicant.created_date_time_ts
        return None