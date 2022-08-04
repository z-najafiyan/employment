# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rolepermissions.roles import assign_role

from candidate.models import (Candidate, MarkedAnnouncement, Education, JobBenefits, JobPreference, Resume,
                              WorkExperience, PersonalInfo, Language)
from candidate.serializers import (CandidateUserPostSerializer, CandidateAnnouncementListSerializer,
                                   CandidateAnnouncementDetailSerializer, CandidateMarkedAnnouncementPostSerializer,
                                   CandidateAnnouncementPatchSerializer,
                                   CandidateEducationPOSTSerializer, CandidateEducationGETSerializer,
                                   CandidateSkillSerializer, CandidateJobPreferencePostSerializer,
                                   CandidateJobPreferenceGetSerializer, CandidateResumeGETSerializer,
                                   CandidateWorkExperiencePostSerializer, CandidateWorkExperienceGetSerializer,
                                   CandidateCompanyListSerializer, CandidateCompanyDetailSerializer,
                                   CandidateSerializer, CandidateResumePatchSerializer,
                                   CandidatePersonalInfoPostSerializer, CandidatePersonalInfoGETSerializer,
                                   CandidateUserSerializer, CandidateLanguagePostSerializer,
                                   CandidateLanguageGetSerializer, CandidateProfessionalSkillSerializer,
                                   CandidateApplicantCreateSerializer)
from candidate.swagger import (swagger_kwargs)
from common.models import Skill, User
from employer.filters import AnnouncementFilter
from employer.models import Announcement, Company
from other_files.helper import FactoryGetObject
from other_files.permissions import IsCandidate


class CandidateView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    # def get_permissions(self):
        # if self.action in ["sing_up", "sing_in", "announcement_list", "new_announcement"]:
        #     self.permission_classes = [AllowAny]
        # else:
        #     self.permission_classes = [IsAuthenticated, IsCandidate]
        #
        # return super(CandidateView, self).get_permissions()

    @swagger_auto_schema(**swagger_kwargs["sing_up"])
    @action(methods=["POST"], detail=False)
    def sing_up(self, request):
        serializer = CandidateUserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(username=serializer.validated_data["email"])
        resume = Resume.objects.create()
        _ = Candidate.objects.create(user=user, resume=resume)
        assign_role(user, "candidate")

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(res, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**swagger_kwargs["sing_in"])
    @action(methods=["POST"], detail=False)
    def sing_in(self, request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = User.objects.get(email=email, )
        except ObjectDoesNotExist:
            return Response([{"user": "email not valid"}], status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response([{"user": "password not valid"}], status=status.HTTP_404_NOT_FOUND)

        try:
            _ = Candidate.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response([{"user": "email or password not valid"}], status=status.HTTP_404_NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(res, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["user"])
    @action(methods=["PATCH"], detail=False)
    def user(self, request):
        user = request.user
        if "mobile" in request.data:
            mobile = request.data.pop("mobile")
            candidate = FactoryGetObject.find_object(Candidate, user=request.user)
            candidate.mobile = mobile
            candidate.save()
        serializer = CandidateUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**swagger_kwargs["candidate"])
    @action(methods=["GET"], detail=False)
    def candidate(self, request):
        user = request.user
        candidate = FactoryGetObject.find_object(Candidate, user=user)
        serializer = CandidateSerializer(candidate)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["resume_get"])
    @swagger_auto_schema(**swagger_kwargs["resume_patch"])
    @action(methods=["GET", "PATCH"], detail=False)
    def resume(self, request):
        if request.method == "GET":
            candidate = FactoryGetObject.find_object(Candidate, user=request.user)
            serializer = CandidateResumeGETSerializer(candidate.resume)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            candidate = FactoryGetObject.find_object(Candidate, user=request.user)
            serializer = CandidateResumePatchSerializer(candidate.resume, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            serializer_res = CandidateResumeGETSerializer(obj)
            return Response(serializer_res.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["education_delete"])
    @swagger_auto_schema(**swagger_kwargs["education_get"])
    @swagger_auto_schema(**swagger_kwargs["education_post"])
    @action(methods=["POST", "GET", "PATCH", "DELETE"], detail=True)
    def education(self, request, pk):

        if request.method == "POST":
            """
            Create education for candidate resume
                :params request: {"field_of_study", "name_university", "grade", "start_date","end_date" 
                                  "is_student","description", "resumes"}
                :param pk:0
                :return:{"id","field_of_study", "name_university", "grade", "start_date","end_date", 
                         "is_student","description", "resumes"}
            """

            serializer = CandidateEducationPOSTSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            """
                 Update education for candidate resume
                     :params request: {"field_of_study", "name_university", "grade","start_date","end_date", 
                                       "is_student","description"}
                     :param pk: id education
                     :return:{"id","field_of_study", "name_university", "grade", "start_date","end_date", 
                              "is_student","description", "resumes"}
            """

            education = FactoryGetObject.find_object(Education, pk=pk)
            serializer = CandidateEducationPOSTSerializer(data=request.data, instance=education, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            """
             detail and list education for candidate resume
                 :param pk: id education
                 :return:{"id","field_of_study", "name_university", "grade", "start_date","end_date" 
                          "is_student","description", "resumes"}
                :query params: state params
            """
            state = request.GET.get("state")
            if state == "list":
                candidate = FactoryGetObject.find_object(Candidate, user=request.user)
                if candidate.resume:
                    education = candidate.resume.education.all()
                    # page = self.paginate_queryset(education)
                    # res = self.get_paginated_response(data=CandidateEducationGETSerializer(page, many=True).data).data
                    res = CandidateEducationGETSerializer(education, many=True).data
                    return Response(res)
            elif state == "detail":
                education = FactoryGetObject.find_object(Education, pk=pk)
                serializer = CandidateEducationGETSerializer(education)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            education = FactoryGetObject.find_object(Education, pk=pk)
            education.delete()
            return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger_kwargs["skill_post"])
    @swagger_auto_schema(**swagger_kwargs["skill_get"])
    @swagger_auto_schema(**swagger_kwargs["skill_delete"])
    @action(methods=["POST", "GET", "PATCH", "DELETE"], detail=True)
    def professional_skills(self, request, pk):
        if request.method == "POST":
            """
            Create skill for candidate resume
                :params request: {"name" ,"resumes"}
                :param pk:0
                :return:{"id","name" ,"resumes"}
            """
            serializer = CandidateProfessionalSkillSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            """
            update skill for candidate resume
                :params request: {"name"}
                :param pk:id
                :return:{"id","name" ,"resumes"}
            """
            skill = FactoryGetObject.find_object(Skill, pk=pk)
            serializer = CandidateSkillSerializer(data=request.data, instance=skill, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            """
            detail and list skill for candidate resume
                :param pk: id skill
                :return:{"id","name", "resumes"}
               :query params: state params
            """
            state = request.GET.get("state")
            if state == "list":
                candidate = FactoryGetObject.find_object(Candidate, user=request.user)
                if candidate.resume:
                    skill = candidate.resume.skill.all()
                    # page = self.paginate_queryset(education)
                    # res = self.get_paginated_response(data=CandidateSkillSerializer(page, many=True).data).data
                    res = CandidateSkillSerializer(skill, many=True).data
                    return Response(res)
            elif state == "detail":
                skill = FactoryGetObject.find_object(Skill, pk=pk)
                serializer = CandidateSkillSerializer(skill)
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            skill = FactoryGetObject.find_object(Skill, pk=pk)
            skill.delete()
            return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger_kwargs["job_preference_post"])
    @swagger_auto_schema(**swagger_kwargs["job_preference_get"])
    @swagger_auto_schema(**swagger_kwargs["job_preference_delete"])
    @action(methods=["POST", "GET", "PATCH", "DELETE"], detail=True)
    def job_preference(self, request, pk):
        if request.method == "POST":
            serializer = CandidateJobPreferencePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            job_benefits = FactoryGetObject.find_object(JobBenefits, pk=pk)
            serializer = CandidateJobPreferencePostSerializer(data=request.data, instance=job_benefits)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            job_preferences = FactoryGetObject.find_object(JobPreference, pk=pk)
            serializer = CandidateJobPreferenceGetSerializer(job_preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            skill = FactoryGetObject.find_object(Skill, pk=pk)
            skill.delete()
            return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)
    @swagger_auto_schema(**swagger_kwargs["language_post"])
    @swagger_auto_schema(**swagger_kwargs["language_get"])
    @swagger_auto_schema(**swagger_kwargs["language_delete"])
    @action(methods=["POST", "GET", "PATCH", "DELETE"], detail=True)
    def language(self, request, pk):
        if request.method == "POST":
            serializer = CandidateLanguagePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            job_benefits = FactoryGetObject.find_object(Language, pk=pk)
            serializer = CandidateLanguagePostSerializer(data=request.data, instance=job_benefits)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            job_preferences = FactoryGetObject.find_object(Language, pk=pk)
            serializer = CandidateLanguageGetSerializer(job_preferences)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            language = FactoryGetObject.find_object(Language, pk=pk)
            language.delete()
            return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)
    @swagger_auto_schema(**swagger_kwargs["work_experience_post"])
    @swagger_auto_schema(**swagger_kwargs["work_experience_get"])
    @swagger_auto_schema(**swagger_kwargs["work_experience_delete"])
    @action(methods=["POST", "GET", "PATCH", "DELETE"], detail=True)
    def work_experience(self, request, pk):
        if request.method == "POST":
            serializer = CandidateWorkExperiencePostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            work_experience = FactoryGetObject.find_object(WorkExperience, pk=pk)
            serializer = CandidateWorkExperiencePostSerializer(data=request.data, instance=work_experience,
                                                               partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            state = request.GET.get("state")
            if state == "list":
                candidate = FactoryGetObject.find_object(Candidate, user=request.user)
                if candidate.resume:
                    work_experience = candidate.resume.work_experience.all()
                    res = CandidateWorkExperienceGetSerializer(work_experience, many=True).data
                    # page = self.paginate_queryset(education)
                    # res = self.get_paginated_response(data=(page, many=True).data).data
                    return Response(res)
                else:
                    return Response(list())
            elif state == "detail":
                work_experience = FactoryGetObject.find_object(WorkExperience, pk=pk)
                res = CandidateWorkExperienceGetSerializer(work_experience).data
                return Response(res)
        else:
            work_experience = FactoryGetObject.find_object(WorkExperience, pk=pk)
            work_experience.delete()
            return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger_kwargs["personal_info_post"])
    @swagger_auto_schema(**swagger_kwargs["personal_info_get"])
    @swagger_auto_schema(**swagger_kwargs["personal_info_delete"])
    @action(methods=["POST", "GET", "PATCH"], detail=True)
    def personal_info(self, request, pk):
        if request.method == "POST":
            serializer = CandidatePersonalInfoPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "PATCH":
            personal_info = FactoryGetObject.find_object(PersonalInfo, pk=pk)
            serializer = CandidatePersonalInfoPostSerializer(data=request.data, instance=personal_info,
                                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "GET":

            personal_info = FactoryGetObject.find_object(PersonalInfo, pk=pk)
            res = CandidatePersonalInfoGETSerializer(personal_info).data
            return Response(res)
        # else:
        #     personal_info = FactoryGetObject.find_object(PersonalInfo, pk=pk)
        #     personal_info.delete()
        #     return Response({'message': "done"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger_kwargs["announcement_list"])
    @action(methods=["GET"], detail=False)
    def announcement_list(self, request):
        query_params = request.query_params
        announcement = Announcement.objects.all()
        data = AnnouncementFilter(queryset=announcement, data=query_params).qs
        page = self.paginate_queryset(data)
        response = self.get_paginated_response(CandidateAnnouncementListSerializer(page, many=True).data).data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["announcement_detail"])
    @action(methods=["GET"], detail=True)
    def announcement_detail(self, request, pk):
        announcement = FactoryGetObject.find_object(Announcement, pk=pk)
        serializer = CandidateAnnouncementDetailSerializer(announcement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["marked_announcement_get"])
    @swagger_auto_schema(**swagger_kwargs["marked_announcement_post"])
    @action(methods=["GET", "POST", "DELETE"], detail=True)
    def marked_announcement(self, request, pk):
        if request.method == "GET":
            marked_announcement = MarkedAnnouncement.objects.filter(candidate__user=request.user).first()
            announcements = marked_announcement.announcement.all()
            page = self.paginate_queryset(announcements)
            response = self.get_paginated_response(CandidateAnnouncementListSerializer(page, many=True).data).data
            return Response(response, status=status.HTTP_200_OK)

        elif request.method == "POST":
            serializer = CandidateMarkedAnnouncementPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            marked_announcement, _ = MarkedAnnouncement.objects.get_or_create(candidate__user=request.user)
            # mark_filter=marked_announcement.announcement.filter(announcement=serializer.validated_data["announcement"])
            # if mark_filter :
            #     marked_announcement.announcement.remove(serializer.validated_data["announcement"])
            # else:
            marked_announcement.announcement.add(serializer.validated_data["announcement"])
            return Response({"message": "done"}, status=status.HTTP_201_CREATED)
        else:
            announcement_obj = FactoryGetObject.find_object(Announcement, pk=pk)
            marked_announcement = MarkedAnnouncement.objects.filter(candidate__user=request.user).first()
            marked_announcement.announcement.remove(announcement_obj)
            return Response({"message": "done"}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**swagger_kwargs["my_announcements"])
    @action(methods=["GET"], detail=False)
    def my_announcements(self, request):
        state = request.GET.get("state", None)
        if state and state == "all":
            announcements = Announcement.objects.filter(applicant__candidate__user=request.user)
        else:
            announcements = Announcement.objects.filter(applicant__candidate__user=request.user,
                                                        applicant__applicant_status=state)
        page = self.paginate_queryset(announcements)
        response = self.get_paginated_response(CandidateAnnouncementListSerializer(page, many=True).data).data
        return Response(response, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False)
    def new_announcement(self, request):
        announcement = Announcement.objects.all()[:9]
        response = CandidateAnnouncementListSerializer(announcement, many=True).data
        return Response(response, status=status.HTTP_200_OK)

    @swagger_auto_schema(**swagger_kwargs["send_resume"])
    @action(methods=["patch"], detail=True)
    def send_resume(self, request, pk):
        announcement = FactoryGetObject.find_object(Announcement, pk=pk)
        serializer = CandidateApplicantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance=serializer.save()
        announcement.applicant.add(instance)
        announcement.save()
        return Response({'message':"ok"}, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False)
    def company(self, request, pk):
        state = request.GET.get("state")
        if state == "list":
            company = Company.objects.all()
            page = self.paginate_queryset(company)
            res = self.get_paginated_response(data=CandidateCompanyListSerializer(page).data).data
            return Response(res)
        elif state == "detail":
            company = FactoryGetObject.find_object(Company, pk=pk)
            serializer = CandidateCompanyDetailSerializer(company)
            return Response(serializer.data)
        else:
            return Response({"message": "state is not define"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["GET"], detail=False)
    def resume_quality(self):
        pass

