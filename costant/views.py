from collections import OrderedDict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from constant import (TYPE_COOPERATION,
                      DEGREE_OF_EDUCATIONS,
                      GENDER,
                      MILITARY_SERVICE,
                      CATEGORY,
                      APPLICANT_STATUS,
                      ANNOUNCEMENT_STATUS,
                      MARITAL_STATUS,
                      MONTH,
                      GRADE,
                      MASTERY_LEVEL,
                      LANGUAGE_NAME,
                      LEVEL,
                      SALARY,
                      JOB_BENEFITS)


class Constant(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    def constant_refactor(constant_tuple, default=None):
        dic = OrderedDict(constant_tuple)
        data = {'count': len(constant_tuple),
                'results': [{'en_name': a[0], 'fa_name': a[1]} for a in dic.items()]}
        if default is not None:
            data.update({'default': {'en_name': default, 'fa_name': dic[default]}})
        else:
            data.update({'default': None})
        return data

    @action(methods=['get'], detail=False)
    def type_cooperation(self, request):
        return Response(self.constant_refactor(TYPE_COOPERATION, 'full_time'))

    @action(methods=['get'], detail=False)
    def degree_of_educations(self, request):
        return Response(self.constant_refactor(DEGREE_OF_EDUCATIONS, 'bachelor'))

    @action(methods=['get'], detail=False)
    def gender(self, request):
        return Response(self.constant_refactor(GENDER, None))

    @action(methods=['get'], detail=False)
    def military_service(self, request):
        return Response(self.constant_refactor(MILITARY_SERVICE, None))

    @action(methods=['get'], detail=False)
    def category(self, request):
        return Response(self.constant_refactor(CATEGORY, None))

    @action(methods=['get'], detail=False)
    def applicant_status(self, request):
        return Response(self.constant_refactor(APPLICANT_STATUS, 'not_checked'))

    @action(methods=['get'], detail=False)
    def announcement_status(self, request):
        return Response(self.constant_refactor(ANNOUNCEMENT_STATUS, None))

    @action(methods=['get'], detail=False)
    def marital_status(self, request):
        return Response(self.constant_refactor(MARITAL_STATUS, None))

    @action(methods=['get'], detail=False)
    def month(self, request):
        return Response(self.constant_refactor(MONTH, None))

    @action(methods=['get'], detail=False)
    def grade(self, request):
        return Response(self.constant_refactor(GRADE, None))

    @action(methods=['get'], detail=False)
    def mastery_level(self, request):
        return Response(self.constant_refactor(MASTERY_LEVEL, None))

    @action(methods=['get'], detail=False)
    def language_name(self, request):
        return Response(self.constant_refactor(LANGUAGE_NAME, "5"))

    @action(methods=['get'], detail=False)
    def level(self, request):
        return Response(self.constant_refactor(LEVEL, None))

    @action(methods=['get'], detail=False)
    def salary(self, request):
        return Response(self.constant_refactor(SALARY, 'agreement'))

    @action(methods=['get'], detail=False)
    def job_benefits(self, request):
        return Response(self.constant_refactor(JOB_BENEFITS, None))
