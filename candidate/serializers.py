from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from candidate.models import (MarkedAnnouncement, Education, JobPreference, Resume, WorkExperience, PersonalInfo,
                              Candidate, Language, ProfessionalSkill)
from common.models import (User, Skill)
from employer.models import (Announcement, Company, Applicant)
from other_files.response_serialzer import (ProvinceResponseSerializer, UserResponseSerializer,
                                            CategoryResponseSerializer,
                                            CityResponseSerializer, ActivityResponseSerializer, )


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


# class CandidateUserSerializer(serializers.ModelSerializer):
#     mobile = serializers.CharField(max_length=11, allow_null=True, )
#
#     class Meta:
#         model = User
#         fields = ["email", "mobile"]


class CandidateSerializer(serializers.ModelSerializer):
    user = UserResponseSerializer()

    class Meta:
        model = Candidate
        fields = ["user", "resume"]


class CandidatePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["mobile", "email"]


class CandidateEducationPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "field_of_study", "name_university", "grade", "start_date", "end_date", "is_student",
                  "description",
                  ]


class CandidateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class CandidateProfessionalSkillSerializer(WritableNestedModelSerializer):
    # skill = CandidateSkillSerializer()

    class Meta:
        model = ProfessionalSkill
        fields = ["id", "skill", "mastery_level",
                  # "resumes"]
                  ]


class CandidateProfessionalSkillGetSerializer(serializers.ModelSerializer):
    # skill = CandidateSkillSerializer()
    mastery_level = serializers.SerializerMethodField()

    class Meta:
        model = ProfessionalSkill
        fields = ["id", "skill", "mastery_level", ]

    def get_mastery_level(self, obj):
        if obj.mastery_level:
            return {"en_name": obj.mastery_level,
                    "fa_name": obj.get_mastery_level_display()}
        return None


class CandidateJobPreferencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPreference
        fields = ["province", "type_cooperation", "mastery_level", "minimum_salary", "degree_of_educations",
                  "id"]


class CandidateLanguagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "mastery_level",]


class CandidateLanguageGetSerializer(serializers.ModelSerializer):
    mastery_level = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = ["id", "name", "mastery_level"]

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


class CandidateJobPreferenceGetSerializer(serializers.ModelSerializer):
    province = ProvinceResponseSerializer()
    # job_benefits = JobBenefitsResponseSerializer(many=True)
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
    start_date = serializers.IntegerField(source="start_date_ts", default=None)
    end_date = serializers.IntegerField(source="end_date_ts", default=None)

    class Meta:
        model = Education
        fields = ["id", "field_of_study", "name_university", "grade", "start_date", "end_date", "is_student",
                  "description", ]

    def get_grade(self, obj):
        return {"en_name": obj.grade,
                "fa_name": obj.get_grade_display()}


class CandidatePersonalInfoGETSerializer(serializers.ModelSerializer):
    # province = ProvinceResponseSerializer()
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
    start_date = serializers.IntegerField(source="start_date_ts", default=None)
    end_date = serializers.IntegerField(source="end_date_ts", default=None)

    class Meta:
        model = WorkExperience
        fields = "__all__"


class CandidateWorkExperiencePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ["id", "job_title", "company_name", "start_date", "end_date",
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
    education = CandidateEducationGETSerializer(many=True)
    personal_info = CandidatePersonalInfoGETSerializer()
    professional_skill = CandidateProfessionalSkillGetSerializer(many=True)
    job_preferences = CandidateJobPreferenceGetSerializer()
    work_experience = CandidateWorkExperienceGetSerializer(many=True)
    file = serializers.CharField(source="link", allow_null=True)
    email = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()
    language = CandidateLanguageGetSerializer(many=True)

    class Meta:
        model = Resume
        fields = ["id", "file", "education", "personal_info", "professional_skill", "job_preferences",
                  "work_experience",
                  "about_me", "language", "mobile", "email"]

    def get_category(self, obj):
        if obj.category:
            res = {"en_name": obj.category,
                   "fa_name": obj.get_category_display()}

        return None

    def get_mobile(self, obj):
        return obj.candidates.mobile

    def get_email(self, obj):
        return obj.candidates.email

    def get_file(self, obj):
        return None


class CandidateResumePatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["about_me"]


class CandidatePersonalInfoPostSerializer(WritableNestedModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ["category", "full_name", "marital_status", "military_status", "address", "years_birth", "gender",
                  "marital_status", ]


class CandidateCompanyListSerializer(serializers.ModelSerializer):
    logo = serializers.CharField(source="link", allow_null=True)
    activity = ActivityResponseSerializer()

    class Meta:
        model = Company
        fields = ["id", 'persian_name', "english_name", "logo", "activity", "description"]


class CandidateAnnouncementListSerializer(serializers.ModelSerializer):
    category = CategoryResponseSerializer()
    company = CandidateCompanyListSerializer()
    province = ProvinceResponseSerializer()
    city = CityResponseSerializer()
    creation_date = serializers.IntegerField(source="creation_date_ts", allow_null=True)
    type_cooperation = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ["id", "category", "creation_date", "title", "province", "city", "type_cooperation", "minimum_salary",
                  "company"]

    def get_type_cooperation(self, obj):
        if obj.type_cooperation:
            return {"en_name": obj.type_cooperation,
                    "fa_name": obj.get_type_cooperation_display()}
        return None


class CandidateCompanyDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CandidateAnnouncementDetailSerializer(serializers.ModelSerializer):
    company = CandidateCompanyListSerializer()
    province = ProvinceResponseSerializer()
    city = CityResponseSerializer()
    type_cooperation = serializers.SerializerMethodField()
    military_service = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    years_work_experience = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ["id", "title", "province", "city", "type_cooperation", "minimum_salary", "gender",
                  "company", "military_service", "description", "years_work_experience"]

    def get_type_cooperation(self, obj):
        if obj.type_cooperation:
            return {"en_name": obj.type_cooperation,
                    "fa_name": obj.get_type_cooperation_display()}
        return None

    def get_military_service(self, obj):
        if obj.military_service:
            return {"en_name": obj.military_service,
                    "fa_name": obj.get_military_service_display()}
        return None

    def get_gender(self, obj):
        if obj.gender:
            return {"en_name": obj.gender,
                    "fa_name": obj.get_gender_display()}
        return None

    def get_years_work_experience(self, obj):
        if obj.years_work_experience:
            return {"en_name": obj.years_work_experience,
                    "fa_name": obj.get_years_work_experience_display()}
        return None


class CandidateMarkedAnnouncementPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkedAnnouncement
        fields = ["announcement"]


class CandidateApplicantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['candidate']


class CandidateAnnouncementPatchSerializer(WritableNestedModelSerializer):
    applicant = CandidateApplicantCreateSerializer()

    class Meta:
        model = Announcement
        fields = ["applicant"]


class CandidateResumePatchV2Serializer(WritableNestedModelSerializer):
    education = CandidateEducationPOSTSerializer(many=True)
    personal_info = CandidatePersonalInfoPostSerializer()
    professional_skill = CandidateProfessionalSkillSerializer(many=True)
    job_preferences = CandidateJobPreferencePostSerializer()
    work_experience = CandidateWorkExperiencePostSerializer(many=True)
    language = CandidateLanguagePostSerializer(many=True)
    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=11)

    class Meta:
        model = Resume
        fields = ["file", "education", "personal_info", "professional_skill", "job_preferences", "work_experience",
                  "about_me", "language", "email", "mobile"]
