from drf_yasg import openapi

from employer.serializers import EmployerUserPostSerializer, EmployerCompanyGetSerializer, \
    EmployerCompanyPostSerializer, EmployerAnnouncementPostSerializer, EmployerAnnouncementGetSerializer, \
    EmployerApplicantPatchSerializer, EmployerCandidateDeleteSerializer, EmployerSerializer, \
    EmployerUserPostV2Serializer
from other_files.response_serialzer import UserTokenSwaggerSerializer

state_param = openapi.Parameter('state', openapi.IN_QUERY, description="state manual param", type=openapi.TYPE_STRING)

swagger_kwargs = {
    "sing_up": {
        "method": "POST",
        "request_body": EmployerUserPostSerializer,
        "responses": {200: UserTokenSwaggerSerializer, }
    },
    "sing_in": {
        "method": "POST",
        "request_body": EmployerUserPostV2Serializer,
        "responses": {200: UserTokenSwaggerSerializer, }
    },
    "employer": {
        "method": "GET",
        "responses": {200: EmployerSerializer, }},
    "company_get": {
        "method": "GET",
        "responses": {201: EmployerCompanyGetSerializer()}},
    "company_patch": {
        "method": "PATCH",
        "request_body": EmployerCompanyPostSerializer,
        "responses": {201: EmployerCompanyPostSerializer()}},
    "announcement_get": {
        "method": "GET",
        "manual_parameters": [state_param],

        "responses": {201: EmployerAnnouncementGetSerializer()}},
    "announcement_post": {
        "methods": ["POST", "PATCH"],
        "request_body": EmployerAnnouncementPostSerializer,
        "responses": {201: EmployerAnnouncementPostSerializer()}},

    "applicant_get": {
        "method": "GET",
        "responses": {201: EmployerApplicantPatchSerializer()}},
    "applicant_patch": {
        "method": "PATCH",
        "request_body": EmployerApplicantPatchSerializer,
        "responses": {201: EmployerApplicantPatchSerializer()}},
    "candidate": {
        "method": "GET",
        "responses": {201: EmployerCandidateDeleteSerializer()}},

    "rejected": {
        "method": "GET",
    },
    "confirmation": {
        "method": "GET",
    },
    "hired": {
        "method": "GET",
    },
    "awaiting_status": {
        "method": "GET",
    }
}
