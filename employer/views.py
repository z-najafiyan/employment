# Create your views here.
import datetime

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.roles import assign_role

from candidate.models import Candidate
from common.models import User
from employer.filters import ApplicantFilter
from employer.models import Company, Employer, Announcement, Applicant, StatusLog
from employer.serializers import (EmployerUserPostSerializer, EmployerCompanyPostSerializer,
                                  EmployerCompanyGetSerializer, EmployerAnnouncementPostSerializer,
                                  EmployerAnnouncementListSerializer, EmployerApplicantGetSerializer,
                                  EmployerAnnouncementGetSerializer, EmployerCandidateDeleteSerializer,
                                  EmployerApplicantPatchSerializer, EmployerSerializer, EmployerUserPostV2Serializer)
from employer.swagger import swagger_kwargs
from other_files.helper import FactoryGetObject
from other_files.permissions import IsEmployer


class EmployerView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # def get_permissions(self):
    #     if self.action in ["sing_up", "sing_in"]:
    #         self.permission_classes = [AllowAny]
    #     else:
    #         self.permission_classes = [IsAuthenticated, IsEmployer]
    #
    #     return super(EmployerView, self).get_permissions()

    @swagger_auto_schema(**swagger_kwargs["sing_up"])
    @action(methods=["POST"], detail=False)
    def sing_up(self, request):
        serializer = EmployerUserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(username=serializer.validated_data["email"])
        company = Company.objects.create()
        _ = Employer.objects.create(user=user, company=company)
        assign_role(user, "employer")

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(res, status=status.HTTP_201_CREATED)
    @swagger_auto_schema(**swagger_kwargs["sing_in"])
    @action(methods=["POST"], detail=False)
    def sing_in(self, request):
        serializer=EmployerUserPostV2Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response([{"user": "email not valid"}], status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response([{"user": "password not valid"}], status=status.HTTP_404_NOT_FOUND)
        try:
            _ = Employer.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response([{"user": "email not valid"}], status=status.HTTP_404_NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(res, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["employer"])
    @action(methods=["GET"], detail=False)
    def employer(self, request):
        user = User.objects.get(pk=2)
        # user = request.user
        employer = FactoryGetObject.find_object(Employer,user=user )
        serializer = EmployerSerializer(employer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["company_get"])
    @swagger_auto_schema(**swagger_kwargs["company_patch"])
    @action(methods=["GET", "PATCH"], detail=True, parser_classes=[FormParser, MultiPartParser])
    def company(self, request, pk):
        if request.method == "PATCH":
            company = FactoryGetObject.find_object(Company, pk=pk)
            serializer = EmployerCompanyPostSerializer(company, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            # user = request.user
            user = User.objects.get(pk=2)
            company = FactoryGetObject.find_object(Company, pk=pk)
            serializer = EmployerCompanyGetSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["announcement_get"])
    @swagger_auto_schema(**swagger_kwargs["announcement_post"])
    @action(methods=["POST", "GET", "PATCH"], detail=True)
    def announcement(self, request, pk):
        if request.method == "POST":
            user = User.objects.get(pk=2)

            employer = FactoryGetObject.find_object(Employer, user=user)
            serializer = EmployerAnnouncementPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(pk=2)

            serializer.save(creator_user=user, company=employer.company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            announcement = FactoryGetObject.find_object(Announcement, pk=pk)
            serializer = EmployerAnnouncementPostSerializer(announcement, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            state = request.GET.get("state")
            announcement_type=request.GET.get("type")
            if state == "list":
                user = User.objects.get(pk=2)
                employer = FactoryGetObject.find_object(Employer, user=user)
                announcements = Announcement.objects.filter(status_name=announcement_type,company=employer.company)
                page = self.paginate_queryset(announcements)
                res = self.get_paginated_response(EmployerAnnouncementListSerializer(page,many=True).data).data
                return Response(res, status=status.HTTP_200_OK)
            elif state == "detail":
                announcement = FactoryGetObject.find_object(Announcement, pk=pk)
                serializer = EmployerAnnouncementGetSerializer(announcement)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "state was not found"}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(**swagger_kwargs["applicant_get"])
    @swagger_auto_schema(**swagger_kwargs["applicant_patch"])
    @action(methods=["GET", "PATCH"], detail=True)
    def applicant(self, request, pk):
        if request.method == "GET":
            announcement = FactoryGetObject.find_object(Announcement, pk=pk)
            applicants = announcement.applicant
            data = request.GET
            applicant_filter = ApplicantFilter(queryset=applicants, data=data)
            page=self.paginate_queryset(applicant_filter)
            res = self.get_paginated_response(EmployerApplicantGetSerializer(applicant_filter,
                                                                             many=True).data).data
            return Response(res)
        else:
            user = User.objects.get(pk=2)
            announcement = FactoryGetObject.find_object(Announcement, pk=pk)
            applicant = FactoryGetObject.find_object(Applicant, pk=request.data["id"])
            serializer = EmployerApplicantPatchSerializer(applicant, data=request.data)
            obj = serializer.save(created_date_time=datetime.datetime.now())
            _ = StatusLog.objects.create(
                candidate=obj.candidate,
                announcement=announcement,
                applicant_status=obj.applicant_status,
                user=user,
                created_date_time=datetime.datetime.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**swagger_kwargs["candidate"])
    @action(methods=["GET"], detail=True)
    def candidate(self, request, pk):
        candidate = FactoryGetObject.find_object(Candidate, pk=pk)
        serializer = EmployerCandidateDeleteSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["rejected"])
    @action(methods=["GET"], detail=True)
    def rejected(self, request, pk):
        applicant = FactoryGetObject.find_object(Applicant, pk=pk)
        applicant.applicant_status = "rejected"
        applicant.save()
        return Response({"message": "done"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["confirmation"])
    @action(methods=["GET"], detail=True)
    def confirmation(self, request, pk):
        applicant = FactoryGetObject.find_object(Applicant, pk=pk)
        announcement = FactoryGetObject.find_object(Announcement, applicant=applicant)
        applicant.applicant_status = "confirmation_for_interview"
        applicant.save()
        user = User.objects.get(pk=2)

        _ = StatusLog.objects.create(
            candidate=applicant.candidate,
            announcement=announcement,
            applicant_status="confirmation_for_interview",
            user=user, )
        return Response({"message": "done"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["hired"])
    @action(methods=["GET"], detail=True)
    def hired(self, request, pk):
        applicant = FactoryGetObject.find_object(Applicant, pk=pk)
        announcement = FactoryGetObject.find_object(Announcement, applicant=applicant)

        applicant.applicant_status = "hired"
        applicant.save()
        user = User.objects.get(pk=2)
        _ = StatusLog.objects.create(
            candidate=applicant.candidate,
            announcement=announcement,
            applicant_status="hired",
            user=user, )
        return Response({"message": "done"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["awaiting_status"])
    @action(methods=["GET"], detail=True)
    def awaiting_status(self, request, pk):
        applicant = FactoryGetObject.find_object(Applicant, pk=pk)
        announcement = FactoryGetObject.find_object(Announcement, applicant=applicant)
        applicant.applicant_status = "awaiting_status"
        applicant.save()
        # user = request.user
        user = User.objects.get(pk=2)

        _ = StatusLog.objects.create(
            candidate=applicant.candidate,
            announcement=announcement,
            applicant_status="awaiting_status",
            user=user)
        return Response({"message": "done"}, status=status.HTTP_200_OK)
