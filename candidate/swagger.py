from drf_yasg import openapi

from candidate.serializers import (CandidateAnnouncementDetailSerializer, CandidateUserPostSerializer,
                                   CandidateAnnouncementListSerializer, CandidateMarkedAnnouncementPostSerializer,
                                   CandidateResumeGETSerializer, CandidateEducationGETSerializer,
                                   CandidateEducationPOSTSerializer, CandidateSkillSerializer,
                                   CandidateJobPreferencePostSerializer, CandidateJobPreferenceGetSerializer,
                                   CandidateWorkExperienceGetSerializer, CandidateWorkExperiencePostSerializer,
                                   CandidateSerializer, CandidatePersonalInfoPostSerializer,
                                   CandidatePersonalInfoGETSerializer, CandidateResumePatchSerializer,
                                   CandidateUserSingInSerializer, CandidateUserSerializer,
                                   CandidateLanguagePostSerializer, CandidateLanguageGetSerializer,
                                   CandidateAnnouncementPatchSerializer, CandidateApplicantCreateSerializer)
from other_files.response_serialzer import UserTokenSwaggerSerializer

state_param = openapi.Parameter('state', openapi.IN_QUERY, description="state manual param", type=openapi.TYPE_STRING)
several_variable = openapi.Parameter('several_variable', openapi.IN_QUERY, description="several_variable manual param", type=openapi.TYPE_STRING)
province = openapi.Parameter('province', openapi.IN_QUERY, description="province manual param", type=openapi.TYPE_STRING)

swagger_kwargs = {
    "sing_up": {
        "method": "POST",
        "request_body": CandidateUserPostSerializer,
        "responses": {201: UserTokenSwaggerSerializer()}},
    "sing_in": {
        "method": "POST",
        "request_body": CandidateUserSingInSerializer,
        "responses": {201: UserTokenSwaggerSerializer()}},
    "candidate": {"method": "GET",
                  "responses": {201: CandidateSerializer()}},
    "resume_get": {"method": "GET",
                   "responses": {201: CandidateResumeGETSerializer()}},
    "resume_patch": {"method": "PATCH",
                     "request_body": CandidateResumePatchSerializer,
                     "responses": {201: CandidateResumeGETSerializer()}},
    "education_get": {
        "method": "GET",
        "manual_parameters": [state_param],
        "responses": {200: CandidateEducationGETSerializer()}},
    "education_post": {
        "methods": ["POST", "PATCH"],
        "request_body": CandidateEducationPOSTSerializer,
        "responses": {200: CandidateEducationGETSerializer()}},
    "education_delete": {
        "method": "DELETE",
    },
    "skill_get": {
        "method": "GET",
        "manual_parameters": [state_param],

        "responses": {200: CandidateSkillSerializer()}},
    "skill_post": {
        "methods": ["POST", "PATCH"],
        "request_body": CandidateSkillSerializer,
        "responses": {200: CandidateSkillSerializer()}},
    "skill_delete": {
        "method": "DELETE",
    },
    "job_preference_get": {
        "method": "GET",
        "responses": {200: CandidateJobPreferenceGetSerializer()}},
    "job_preference_post": {
        "methods": ["POST", "PATCH"],
        "request_body": CandidateJobPreferencePostSerializer,
        "responses": {200: CandidateJobPreferenceGetSerializer()}},
    "job_preference_delete": {
        "method": "DELETE",
    },

    "work_experience_get": {
        "method": "GET",
        "manual_parameters": [state_param],

        "responses": {200: CandidateWorkExperienceGetSerializer()}},
    "work_experience_post": {
        "methods": ["POST", "PATCH"],
        "request_body": CandidateWorkExperiencePostSerializer,
        "responses": {200: CandidateWorkExperienceGetSerializer()}},
    "work_experience_delete": {
        "method": "DELETE",
    },
    "personal_info_get": {
        "method": "GET",
        "responses": {200: CandidatePersonalInfoGETSerializer()}},
    "personal_info_post": {
        "methods": ["POST", "PATCH"],
        "request_body": CandidatePersonalInfoPostSerializer,
        "responses": {200: CandidatePersonalInfoPostSerializer()}},
    "personal_info_delete": {
        "method": "DELETE",
    },
    "announcement_list": {"method": "GET",
                          "manual_parameters": [several_variable,province],

                          "responses": {200: CandidateAnnouncementListSerializer()}},
    "announcement_detail": {"method": "GET",
                            "responses": {200: CandidateAnnouncementDetailSerializer()}},
    "marked_announcement_get": {
        "method": "GET",
        "responses": {200: CandidateAnnouncementListSerializer()}},
    "marked_announcement_post": {
        "method": "POST",
        "request_body": CandidateMarkedAnnouncementPostSerializer,
        "responses": {200: CandidateMarkedAnnouncementPostSerializer()}},
    "marked_announcement_delete": {
        "method": "DELETE",
    },
    "language_get": {
        "method": "GET",
        "responses": {200: CandidateLanguageGetSerializer()}},
    "language_post": {
        "method": "POST",
        "request_body": CandidateLanguagePostSerializer,
        "responses": {200: CandidateLanguagePostSerializer()}},
    "language_delete": {
        "method": "DELETE",
    },
    "user":{"method": "PATCH",
        "request_body": CandidateUserSerializer,
        "responses": {200: CandidateUserSerializer()}},
    "my_announcements": {
        "method": "GET",
        "responses": {200: CandidateAnnouncementListSerializer()}},
    "send_resume": {"method": "PATCH",
             "request_body": CandidateApplicantCreateSerializer,
             },

}

# education = [swagger_kwargs["education_post"], swagger_kwargs["education_get"], swagger_kwargs["education_delete"]]
# skill = [swagger_kwargs["skill_post"], swagger_kwargs["skill_get"], swagger_kwargs["skill_delete"]]
# job_preference = [swagger_kwargs["job_preference_post"], swagger_kwargs["job_preference_get"],
#                   swagger_kwargs["job_preference_delete"]]
# work_experience = [swagger_kwargs["work_experience_post"], swagger_kwargs["work_experience_get"],
#                    swagger_kwargs["work_experience_delete"]]
